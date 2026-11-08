import test from 'node:test';
import assert from 'node:assert/strict';
import { createInitialState, applyCommand, tripCondition, parseTime, formatTime } from '../frontend/domain.js';

const command = (s, type, fields = {}) => applyCommand(s, { type, ...fields });
const returned = (s) => s.trips.find(t => t.id === 'return');
const delayed = () => {
  let s = command(createInitialState(), 'setClock', { now: 1010 });
  return command(s, 'updateTrip', { tripId: 'return', eta: 1065, status: 'en-route' });
};

test('fixtures keep distinct immutable outbound/return schedule and valid service-day time', () => {
  const s = createInitialState();
  assert.equal(s.trips.length, 2);
  assert.notEqual(s.trips[0].windowStart, s.trips[1].windowStart);
  assert.equal(parseTime('17:45'), 1065);
  assert.equal(parseTime(''), null);
  for (const bad of ['24:00', '12:99', '9:30', 'oops']) assert.throws(() => parseTime(bad));
  assert.equal(formatTime(1065), '5:45 PM');
  assert.equal(formatTime(null), 'Estimate unavailable');
});
test('ETA equality, ahead, unknown and terminal status are truthful', () => {
  const t = returned(createInitialState());
  assert.equal(tripCondition({ ...t, eta: t.windowEnd }, 1010).key, 'on-time');
  assert.equal(tripCondition({ ...t, eta: t.windowStart - 1 }, 1010).key, 'ahead');
  assert.equal(tripCondition({ ...t, eta: null }, 1010).key, 'unknown');
  assert.equal(tripCondition({ ...t, status: 'completed', eta: 1200 }, 1010).key, 'completed');
});
test('update is pure, preserves windows, rejects invalid status/time and no-op duplicate', () => {
  const s = createInitialState(); const before = structuredClone(s);
  const t = returned(s);
  const next = command(s, 'updateTrip', { tripId: 'return', eta: 1065, status: 'en-route' });
  assert.deepEqual(s, before);
  assert.equal(returned(next).windowEnd, t.windowEnd);
  assert.equal(returned(next).windowStart, t.windowStart);
  assert.equal(command(next, 'updateTrip', { tripId: 'return', eta: 1065, status: 'en-route' }), next);
  for (const eta of [-1, 1440, 17.5, NaN]) assert.throws(() => command(s, 'updateTrip', { tripId: 'return', eta, status: 'en-route' }));
  assert.throws(() => command(s, 'updateTrip', { tripId: 'return', eta: 1050, status: 'cancelled' }));
  assert.throws(() => command(s, 'setClock', { now: 0 }));
  assert.throws(() => command(s, 'setChannel', { channel: 'real-provider' }));
});
test('early delay notice snapshots ETA/window and starts sent only', () => {
  const s = delayed(); const n = s.notices.at(-1);
  assert.equal(n.kind, 'delay'); assert.equal(n.tripId, 'return');
  assert.equal(n.eta, 1065); assert.equal(n.windowEnd, 1050);
  assert.equal(n.createdAt, 1010); assert.equal(n.earlyNoticeMiss, false);
  assert.equal(n.attempts[0].outcome, 'sent');
  assert.equal(n.attempts[0].deliveredAt, null);
});
test('at-end and late discovery never fabricate early notice', () => {
  for (const now of [1050, 1055]) {
    let s = command(createInitialState(), 'setClock', { now });
    s = command(s, 'updateTrip', { tripId: 'return', eta: 1065, status: 'en-route' });
    assert.equal(s.notices[0].earlyNoticeMiss, true);
    assert.equal(s.notices[0].attempts[0].sentAt, now);
  }
});
test('changed delayed ETA, recovery, unknown and historical snapshots remain distinct', () => {
  const first = delayed();
  const next = command(first, 'updateTrip', { tripId: 'return', eta: 1075, status: 'en-route' });
  assert.equal(next.notices.length, 2); assert.equal(next.notices[0].eta, 1065);
  const recovery = command(next, 'updateTrip', { tripId: 'return', eta: 1040, status: 'en-route' });
  assert.equal(recovery.notices.at(-1).kind, 'recovery');
  const unknown = command(recovery, 'updateTrip', { tripId: 'return', eta: null, status: 'en-route' });
  assert.equal(unknown.notices.at(-1).kind, 'unavailable');
  assert.equal(unknown.notices.at(-1).eta, null);
});
test('terminal trip changes do not create delay notices; clock alone creates none', () => {
  let s = command(createInitialState(), 'setClock', { now: 1100 });
  assert.equal(s.notices.length, 0);
  s = command(s, 'updateTrip', { tripId: 'return', eta: 1200, status: 'completed' });
  assert.equal(s.notices.length, 0);
});
test('driver acceptance gates change notice but not predicted delay', () => {
  const s = createInitialState();
  assert.throws(() => command(s, 'sendChange', { tripId: 'return', accepted: false }));
  assert.equal(command(s, 'sendChange', { tripId: 'return', accepted: true }).notices[0].kind, 'change');
  const next = command(s, 'updateTrip', { tripId: 'return', eta: 1065, status: 'en-route', acceptedChange: true });
  assert.equal(next.notices.length, 1); assert.equal(next.notices[0].kind, 'delay');
});
test('delivery then explicit acknowledgement; invalid transitions rejected', () => {
  let s = delayed(); const noticeId = s.notices[0].id;
  assert.throws(() => command(s, 'setOutcome', { noticeId, outcome: 'acknowledged' }));
  s = command(s, 'setOutcome', { noticeId, outcome: 'delivered' });
  assert.equal(s.notices[0].attempts[0].outcome, 'delivered');
  s = command(s, 'setOutcome', { noticeId, outcome: 'acknowledged' });
  assert.equal(s.notices[0].attempts[0].outcome, 'acknowledged');
  assert.throws(() => command(s, 'setOutcome', { noticeId, outcome: 'unreachable' }));
});
test('unreachable and retry preserve history and do not reschedule; channel affects future attempt', () => {
  let s = delayed(); const tripBefore = structuredClone(s.trips); const noticeId = s.notices[0].id;
  s = command(s, 'setOutcome', { noticeId, outcome: 'unreachable' });
  const attempt = structuredClone(s.notices[0].attempts[0]);
  s = command(s, 'setChannel', { channel: 'phone' });
  s = command(s, 'retryNotice', { noticeId });
  assert.deepEqual(s.notices[0].attempts[0], attempt);
  assert.equal(s.notices[0].attempts[1].channel, 'phone');
  assert.equal(s.notices[0].attempts[1].outcome, 'sent');
  assert.deepEqual(s.trips, tripBefore);
});
test('contact validates 1-500 trimmed characters and preserves trip/snapshot on review', () => {
  const s = delayed(); const before = structuredClone(s.trips);
  for (const message of ['', '   ', 'x'.repeat(501)]) assert.throws(() => command(s, 'contact', { tripId: 'return', message }));
  const next = command(s, 'contact', { tripId: 'return', message: '  This time will not work.  ' });
  assert.equal(next.requests[0].message, 'This time will not work.');
  assert.equal(next.requests[0].eta, 1065);
  const reviewed = command(next, 'reviewRequest', { requestId: next.requests[0].id });
  assert.equal(reviewed.requests[0].reviewed, true); assert.deepEqual(reviewed.trips, before);
  assert.equal(command(reviewed, 'reviewRequest', { requestId: reviewed.requests[0].id }), reviewed);
  assert.equal(command(s, 'contact', { tripId: 'return', message: 'x'.repeat(500) }).requests.length, 1);
});
test('fixture scenarios are deterministic and distinguish late/unknown return states', () => {
  assert.equal(createInitialState('early-delay').notices[0].earlyNoticeMiss, false);
  assert.equal(createInitialState('late-discovery').notices[0].earlyNoticeMiss, true);
  assert.equal(returned(createInitialState('unknown')).eta, null);
  assert.deepEqual(createInitialState('normal'), createInitialState('normal'));
});
