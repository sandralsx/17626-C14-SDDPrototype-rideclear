/** Pure V1 behavior. All times and delivery outcomes are explicit simulation data. */
export const CHANNELS = ['sms', 'phone', 'email'];
export const STATUSES = ['scheduled', 'en-route', 'arrived', 'completed'];
const terminal = status => status === 'arrived' || status === 'completed';
const copy = state => structuredClone(state);
const fail = message => { throw new Error(message); };
const minute = value => Number.isInteger(value) && value >= 0 && value < 1440;

export function parseTime(value) {
  if (value === '') return null;
  if (!/^\d{2}:\d{2}$/.test(value)) fail('Enter a valid time from 00:00 to 23:59.');
  const [h, m] = value.split(':').map(Number);
  if (h > 23 || m > 59) fail('Enter a valid time from 00:00 to 23:59.');
  return h * 60 + m;
}
export function timeInput(value) {
  return value === null ? '' : `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
}
export function formatTime(value) {
  if (value === null) return 'Estimate unavailable';
  const h = Math.floor(value / 60);
  return `${h % 12 || 12}:${String(value % 60).padStart(2, '0')} ${h >= 12 ? 'PM' : 'AM'}`;
}
export const windowLabel = trip => `${formatTime(trip.windowStart)} – ${formatTime(trip.windowEnd)}`;
export function tripCondition(trip) {
  if (trip.status === 'completed') return { key: 'completed', label: 'Trip completed' };
  if (trip.status === 'arrived') return { key: 'arrived', label: 'Vehicle arrived' };
  if (trip.eta === null) return { key: 'unknown', label: 'Estimate unavailable' };
  if (trip.eta > trip.windowEnd) return { key: 'delayed', label: 'Pickup delayed' };
  if (trip.eta < trip.windowStart) return { key: 'ahead', label: 'Ahead of pickup window' };
  return { key: 'on-time', label: 'Within pickup window' };
}

export function createInitialState(scenario = 'normal') {
  let state = {
    schemaVersion: 1, revision: 0, nextId: 1, now: 525,
    serviceDate: '2026-11-07', timezone: 'America/New_York', channel: 'sms', scenario,
    trips: [
      { id: 'outbound', direction: 'Outbound', origin: 'Maple Street home', destination: 'Riverside Community Center', vehicle: 'Accessible van 12', windowStart: 540, windowEnd: 560, eta: 550, status: 'en-route', updatedAt: 520 },
      { id: 'return', direction: 'Return', origin: 'Riverside Community Center', destination: 'Maple Street home', vehicle: 'Accessible van 18', windowStart: 1020, windowEnd: 1050, eta: 1035, status: 'scheduled', updatedAt: 520 }
    ], notices: [], requests: []
  };
  if (scenario !== 'normal') {
    if (!['early-delay', 'late-discovery', 'unknown'].includes(scenario)) fail('Choose a known demo scenario.');
    state.now = scenario === 'late-discovery' ? 1055 : 1010;
    state.trips[0].status = 'completed';
    state = applyCommand(state, { type: 'updateTrip', tripId: 'return', eta: scenario === 'unknown' ? null : 1065, status: 'en-route' });
  }
  return state;
}

function findTrip(state, tripId) {
  return state.trips.find(t => t.id === tripId) || fail('Choose a valid trip leg.');
}
function findNotice(state, id) {
  return state.notices.find(n => n.id === id) || fail('This notification is no longer available. Refresh the view.');
}
function addNotice(state, trip, kind) {
  const n = {
    id: `N${state.nextId++}`, tripId: trip.id, kind, eta: trip.eta,
    windowStart: trip.windowStart, windowEnd: trip.windowEnd, createdAt: state.now,
    earlyNoticeMiss: kind === 'delay' && state.now >= trip.windowEnd,
    attempts: [{ channel: state.channel, sentAt: state.now, outcome: 'sent', deliveredAt: null, acknowledgedAt: null, unreachableAt: null }]
  };
  state.notices.push(n);
}

/** Does not mutate input. The persistence adapter owns revision increments. */
export function applyCommand(state, cmd) {
  if (!cmd || typeof cmd.type !== 'string') fail('Choose a valid action.');
  if (cmd.type === 'reset' || cmd.type === 'loadScenario') {
    const next = createInitialState(cmd.type === 'reset' ? 'normal' : cmd.scenario);
    next.revision = state.revision;
    return next;
  }
  if (cmd.type === 'setClock') {
    if (!minute(cmd.now)) fail('Enter a valid demo time from 00:00 to 23:59.');
    if (cmd.now < state.now) fail('Demo time cannot move backwards. Reset or load a scenario to start again.');
    if (cmd.now === state.now) return state;
    const next = copy(state); next.now = cmd.now; return next;
  }
  if (cmd.type === 'setChannel') {
    if (!CHANNELS.includes(cmd.channel)) fail('Choose SMS, phone or email.');
    if (cmd.channel === state.channel) return state;
    const next = copy(state); next.channel = cmd.channel; return next;
  }
  if (cmd.type === 'updateTrip') {
    const previous = findTrip(state, cmd.tripId);
    if (cmd.eta !== null && !minute(cmd.eta)) fail('Enter a valid ETA or leave the estimate unavailable.');
    if (!STATUSES.includes(cmd.status)) fail('Choose a valid vehicle status.');
    if (previous.eta === cmd.eta && previous.status === cmd.status) return state;
    const next = copy(state); const trip = findTrip(next, cmd.tripId);
    trip.eta = cmd.eta; trip.status = cmd.status; trip.updatedAt = next.now;
    let kind = null;
    if (!terminal(trip.status)) {
      if (trip.eta === null && previous.eta !== null) kind = 'unavailable';
      else if (trip.eta !== null && trip.eta > trip.windowEnd) kind = 'delay';
      else if (previous.eta !== null && previous.eta > trip.windowEnd && trip.eta !== null) kind = 'recovery';
      else if (cmd.acceptedChange === true) kind = 'change';
    }
    if (kind) addNotice(next, trip, kind);
    return next;
  }
  if (cmd.type === 'sendChange') {
    const trip = findTrip(state, cmd.tripId);
    if (cmd.accepted !== true) fail('Record simulated driver acceptance before sending a change notice. Delay notices do not wait for acceptance.');
    const next = copy(state); addNotice(next, trip, 'change'); return next;
  }
  if (cmd.type === 'setOutcome') {
    const notice = findNotice(state, cmd.noticeId); const latest = notice.attempts.at(-1);
    if (!['delivered', 'acknowledged', 'unreachable'].includes(cmd.outcome)) fail('Choose a valid simulated delivery outcome.');
    if (latest.outcome === cmd.outcome) return state;
    const valid = latest.outcome === 'sent' ? ['delivered', 'unreachable'] : latest.outcome === 'delivered' ? ['acknowledged'] : [];
    if (!valid.includes(cmd.outcome)) fail('Record delivery before acknowledgement. A finished attempt cannot be changed; retry an unreachable attempt.');
    const next = copy(state); const attempt = findNotice(next, cmd.noticeId).attempts.at(-1);
    attempt.outcome = cmd.outcome;
    attempt[{ delivered: 'deliveredAt', acknowledged: 'acknowledgedAt', unreachable: 'unreachableAt' }[cmd.outcome]] = next.now;
    return next;
  }
  if (cmd.type === 'retryNotice') {
    const notice = findNotice(state, cmd.noticeId);
    if (notice.attempts.at(-1).outcome !== 'unreachable') fail('Only an unreachable notice can be retried.');
    const next = copy(state);
    findNotice(next, cmd.noticeId).attempts.push({ channel: next.channel, sentAt: next.now, outcome: 'sent', deliveredAt: null, acknowledgedAt: null, unreachableAt: null });
    return next;
  }
  if (cmd.type === 'contact') {
    const trip = findTrip(state, cmd.tripId);
    const message = typeof cmd.message === 'string' ? cmd.message.trim() : '';
    if (message.length < 1 || message.length > 500) fail('Enter a message of 1–500 characters. Spaces alone do not count.');
    const next = copy(state);
    next.requests.push({ id: `R${next.nextId++}`, tripId: trip.id, eta: trip.eta, message, createdAt: next.now, reviewed: false, reviewedAt: null });
    return next;
  }
  if (cmd.type === 'reviewRequest') {
    const request = state.requests.find(r => r.id === cmd.requestId);
    if (!request) fail('This contact request is no longer available. Refresh the view.');
    if (request.reviewed) return state;
    const next = copy(state); const r = next.requests.find(x => x.id === cmd.requestId);
    r.reviewed = true; r.reviewedAt = next.now; return next;
  }
  fail('This action is not supported in the V1 demo.');
}

export function noticeTitle(notice) {
  return { delay: 'Your pickup is delayed', recovery: 'Your estimate is back within the window', unavailable: 'Your arrival estimate is unavailable', change: 'Your pickup information has changed' }[notice.kind];
}
export const channelLabel = channel => ({ sms: 'SMS', phone: 'Phone', email: 'Email' }[channel]);
