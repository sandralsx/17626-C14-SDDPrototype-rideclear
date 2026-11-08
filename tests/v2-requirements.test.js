import test from 'node:test';
import assert from 'node:assert/strict';
import { createInitialState, applyCommand, tripCondition, noticeTiming } from '../frontend/domain.js';

const cmd = (s, type, values = {}) => applyCommand(s, { type, ...values });
const ret = s => s.trips.find(t => t.id === 'return');
const delay = () => createInitialState('early-delay');

test('FR-017 elapsed estimates warn without inventing arrival, history or new input time', () => {
  const initial = createInitialState();
  const later = cmd(initial, 'setClock', { now: 1055 });
  assert.equal(tripCondition(ret(later), later.now).key, 'elapsed');
  assert.equal(ret(later).eta, 1035);
  assert.equal(ret(later).updatedAt, 520);
  assert.equal(ret(later).status, 'scheduled');
  assert.equal(later.notices.length, 0);
  assert.deepEqual(later.trips, initial.trips);
});

test('FR-017 exact ETA, unknown and terminal statuses retain distinct meanings', () => {
  const t = ret(createInitialState());
  assert.equal(tripCondition(t, t.eta).key, 'on-time');
  assert.equal(tripCondition(t, t.eta + 1).key, 'elapsed');
  assert.equal(tripCondition({ ...t, eta: null }, 1100).key, 'unknown');
  assert.equal(tripCondition({ ...t, status: 'arrived' }, 1100).key, 'arrived');
  assert.equal(tripCondition({ ...t, status: 'completed' }, 1100).key, 'completed');
  assert.equal(tripCondition({ ...t, eta: 1065 }, 1055).key, 'delayed');
});

test('FR-010 revised: a changed elapsed ETA never issues a recovery notice', () => {
  const s = cmd(delay(), 'setClock', { now: 1055 });
  const updated = cmd(s, 'updateTrip', { tripId: 'return', eta: 1040, status: 'en-route' });
  assert.equal(updated.notices.at(-1).kind, 'elapsed');
  assert.equal(updated.notices[0].kind, 'delay');
  assert.equal(updated.notices[0].eta, 1065);
  assert.equal(ret(updated).windowEnd, 1050);
  const future = cmd(delay(), 'setClock', { now: 1040 });
  assert.equal(cmd(future, 'updateTrip', { tripId: 'return', eta: 1045, status: 'en-route' }).notices.at(-1).kind, 'recovery');
});

test('FR-018 early discovery plus late delivery cannot imply early recorded delivery', () => {
  let s = cmd(delay(), 'setClock', { now: 1055 });
  s = cmd(s, 'setOutcome', { noticeId: 'N1', outcome: 'delivered' });
  const n = s.notices[0];
  const before = structuredClone(n);
  assert.deepEqual(noticeTiming(n, s.now), { discovery: 'before', delivery: 'late', deliveredAt: 1055, followUp: true });
  assert.deepEqual(n, before);
  assert.equal(n.createdAt, 1010);
  assert.equal(n.attempts[0].sentAt, 1010);
});

test('FR-018 strict-before deadline distinguishes pending, no evidence and exact-end delivery', () => {
  const n = delay().notices[0];
  assert.equal(noticeTiming(n, 1049).delivery, 'pending');
  assert.equal(noticeTiming(n, 1050).delivery, 'missing');
  assert.equal(noticeTiming(n, 1050).followUp, true);
  let s = cmd(delay(), 'setClock', { now: 1050 });
  s = cmd(s, 'setOutcome', { noticeId: 'N1', outcome: 'delivered' });
  assert.equal(noticeTiming(s.notices[0], 1050).delivery, 'late');
  const lateDiscovery = createInitialState('late-discovery');
  assert.equal(noticeTiming(lateDiscovery.notices[0], lateDiscovery.now).discovery, 'late');
});

test('FR-018 early delivery remains early after later acknowledgement; sent is not delivery', () => {
  let s = cmd(delay(), 'setClock', { now: 1040 });
  s = cmd(s, 'setOutcome', { noticeId: 'N1', outcome: 'delivered' });
  s = cmd(s, 'setClock', { now: 1055 });
  s = cmd(s, 'setOutcome', { noticeId: 'N1', outcome: 'acknowledged' });
  assert.equal(noticeTiming(s.notices[0], s.now).delivery, 'before');
  assert.equal(noticeTiming(s.notices[0], s.now).followUp, false);
  assert.equal(s.notices[0].attempts[0].deliveredAt, 1040);
  assert.equal(s.notices[0].attempts[0].acknowledgedAt, 1055);
  assert.equal(noticeTiming(delay().notices[0], 1010).deliveredAt, null);
});

test('FR-018 retry preserves unreachable evidence while using current preference', () => {
  let s = cmd(delay(), 'setOutcome', { noticeId: 'N1', outcome: 'unreachable' });
  assert.equal(noticeTiming(s.notices[0], s.now).followUp, true);
  const old = structuredClone(s.notices[0].attempts[0]);
  s = cmd(s, 'setChannel', { channel: 'phone' });
  s = cmd(s, 'retryNotice', { noticeId: 'N1' });
  assert.deepEqual(s.notices[0].attempts[0], old);
  assert.equal(s.notices[0].attempts[1].channel, 'phone');
  assert.equal(noticeTiming(s.notices[0], 1055).delivery, 'missing');
});

test('V2 comparison fixtures reproduce elapsed and late-delivery evidence deterministically', () => {
  const elapsed = createInitialState('elapsed-eta');
  assert.equal(tripCondition(ret(elapsed), elapsed.now).key, 'elapsed');
  assert.equal(elapsed.notices.length, 0);
  const delivered = createInitialState('late-delivery');
  assert.equal(delivered.notices[0].createdAt, 1010);
  assert.equal(noticeTiming(delivered.notices[0], delivered.now).delivery, 'late');
  assert.deepEqual(createInitialState('late-delivery'), delivered);
});
