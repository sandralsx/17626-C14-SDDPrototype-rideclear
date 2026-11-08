import { createStore } from './store.js';
import { formatTime, timeInput, parseTime, windowLabel, tripCondition, noticeTitle, channelLabel, noticeTiming } from './domain.js';

const store = createStore();
let state = store.read();
let view = 'rider';
let selected = 'outbound';
try { view = sessionStorage.getItem('rideclear-v2-view') === 'dispatch' ? 'dispatch' : 'rider'; selected = sessionStorage.getItem('rideclear-v2-leg') === 'return' ? 'return' : 'outbound'; } catch { /* the app also works without browser persistence */ }
const drafts = new Map();
let busy = false;
const $ = id => document.getElementById(id);
const escape = text => String(text).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
const statusLabel = status => ({ scheduled: 'Scheduled', 'en-route': 'On the way', arrived: 'Vehicle arrived', completed: 'Trip completed' }[status]);
const outcomeLabel = outcome => ({ sent: 'Sent · not yet delivered', delivered: 'Delivered · not yet acknowledged', acknowledged: 'Acknowledged', unreachable: 'Unreachable · follow-up needed' }[outcome]);
const viewRevision = () => `data-revision="${state.revision}"`;
const keyFor = name => `${name}-${selected}`;
function rememberView() { try { sessionStorage.setItem('rideclear-v2-view', view); sessionStorage.setItem('rideclear-v2-leg', selected); } catch {} }
function announce(message, error = false) {
  $('feedback').classList.toggle('error', error);
  $('feedback').textContent = message;
}
function captureFocus() {
  const el = document.activeElement;
  if (!el?.id) return null;
  return { id: el.id, start: el.selectionStart, end: el.selectionEnd };
}
function restoreFocus(saved) {
  if (!saved) return;
  const el = $(saved.id);
  if (!el || el.disabled) return;
  el.focus({ preventScroll: true });
  if (typeof saved.start === 'number' && ['textarea', 'text'].includes(el.type)) {
    try { el.setSelectionRange(saved.start, saved.end); } catch {}
  }
}
function staleHint(key) {
  const draft = drafts.get(key);
  return draft && draft.revision !== state.revision ? `<div class="stale-hint">The demo data changed. Review fresh values before saving.<br><button type="button" data-refresh="${key}">Refresh this form</button></div>` : '';
}

function renderLegs() {
  $('trip-list').innerHTML = state.trips.map(t => {
    const condition = tripCondition(t, state.now);
    return `<button type="button" id="leg-${t.id}" class="trip-button" data-leg="${t.id}" aria-pressed="${selected === t.id}"><span class="direction">${t.direction}<span aria-hidden="true">${t.id === 'outbound' ? '↗' : '↙'}</span></span><span class="route-short">${escape(t.destination)}</span><span class="window-small">${windowLabel(t)}</span><span class="leg-state ${condition.key}">${condition.label}</span></button>`;
  }).join('');
}
function tripPanel(trip) {
  const condition = tripCondition(trip, state.now);
  const etaDescription = trip.eta === null ? 'Dispatch will update your estimate when one is available.'
    : condition.key === 'elapsed' ? 'The recorded estimate has passed. Arrival is not confirmed. Contact dispatch for a new estimate.'
    : condition.key === 'delayed' ? 'Later than your original pickup window. See the latest notice below.'
    : condition.key === 'ahead' ? 'Earlier than the window. Your scheduled pickup window has not changed.'
    : ['arrived', 'completed'].includes(condition.key) ? 'Last recorded estimate. This is not an actual arrival timestamp.'
    : 'The current estimate is within your scheduled pickup window.';
  return `<section class="card pickup-card" aria-labelledby="pickup-heading"><div class="card-header"><div><p class="eyebrow">${trip.direction.toUpperCase()} PICKUP</p><h2 id="pickup-heading">Your pickup details</h2></div><span class="trip-id">${trip.id === 'outbound' ? 'RC-104' : 'RC-105'}</span></div><div class="route"><div class="route-stop"><span>Pickup</span><strong>${escape(trip.origin)}</strong></div><div class="route-stop"><span>Destination</span><strong>${escape(trip.destination)}</strong></div></div><div class="timing"><span class="label">Original scheduled pickup window</span><strong class="saved-window" data-testid="saved-window">${windowLabel(trip)}</strong><div class="eta-block ${condition.key}"><span class="label">${['elapsed', 'arrived', 'completed'].includes(condition.key) ? 'Last recorded estimated arrival' : 'Latest estimated arrival'}</span><strong class="eta ${trip.eta === null ? 'unknown' : ''}" data-testid="current-eta">${formatTime(trip.eta)}</strong><span class="pill ${condition.key}">${condition.label}</span><p style="margin-top:12px">${etaDescription}</p></div></div><div class="vehicle-row"><div><span>Vehicle</span><strong>${escape(trip.vehicle)}</strong></div><div><span>Vehicle status</span><strong>${statusLabel(trip.status)}</strong></div></div><hr class="subtle-rule"><p class="small" style="margin-bottom:0">Estimate updated at <strong>${formatTime(trip.updatedAt)}</strong> · Eastern<br>Both the estimate and the service time are simulated.</p></section>`;
}
function noticeBody(notice) {
  const timing = noticeTiming(notice, state.now);
  const discovery = timing ? `<p class="small">Discovery ${timing.discovery === 'before' ? 'before window end' : 'at or after window end · early-notice miss'}. Window end ${formatTime(notice.windowEnd)}.</p>` : '';
  const labels = {
    before: 'Delivery recorded before window end',
    late: 'Delivery recorded at or after window end · follow-up needed',
    pending: 'Delivery not yet recorded · before-window deadline pending',
    missing: 'No delivery recorded before window end · follow-up needed'
  };
  const evidence = timing ? `<p class="${timing.followUp ? 'late-note' : 'small'}">${labels[timing.delivery]}${timing.followUp && !['late', 'missing'].includes(timing.delivery) ? ' · manual follow-up needed' : ''}. Recorded delivery is not proof of acknowledgement or understanding.</p>` : '';
  return `<p>${notice.tripId === 'return' ? 'Return' : 'Outbound'} trip · ${notice.eta === null ? 'No estimate was recorded.' : `Recorded estimated arrival ${formatTime(notice.eta)}.`}<br>Original window ${windowLabel(notice)}.</p>${discovery}${evidence}`;
}
function attemptHistory(notice) {
  const time = value => value === null ? 'not recorded' : formatTime(value);
  return `<ol class="history">${notice.attempts.map((a, i) => `<li><strong>${channelLabel(a.channel)} · attempt ${i + 1}</strong><br>Sent ${time(a.sentAt)}<br>Delivered ${time(a.deliveredAt)}<br>Acknowledged ${time(a.acknowledgedAt)}<br>Unreachable ${time(a.unreachableAt)}</li>`).join('')}</ol>`;
}
function riderNotices() {
  const notices = state.notices.filter(n => n.tripId === selected).toReversed();
  return `<section class="card" aria-labelledby="notices-heading"><div class="card-header"><h2 id="notices-heading">Trip updates</h2><span class="section-count">${notices.length}</span></div>${notices.length ? notices.map(n => {
    const a = n.attempts.at(-1);
    return `<article class="notice"><div class="notice-meta"><span class="pill ${a.outcome}">${a.outcome === 'acknowledged' ? 'Acknowledged' : a.outcome === 'unreachable' ? 'Unreachable' : a.outcome === 'delivered' ? 'Delivered' : 'Sent'}</span><span class="small">${n.kind === 'delay' ? 'Identified' : 'Created'} ${formatTime(n.createdAt)}</span></div><h3>${noticeTitle(n)}</h3>${noticeBody(n)}<p class="small">${channelLabel(a.channel)} · simulated channel<br>${outcomeLabel(a.outcome)}</p>${attemptHistory(n)}${['delivered', 'acknowledged'].includes(a.outcome) ? `<button type="button" id="ack-${n.id}" aria-disabled="${a.outcome === 'acknowledged'}" data-outcome="acknowledged" data-notice="${n.id}" ${viewRevision()}>${a.outcome === 'acknowledged' ? 'Update acknowledged' : 'Acknowledge this update'}</button>` : ''}</article>`;
  }).join('') : '<div class="empty"><strong>No trip updates yet.</strong><p class="small" style="margin-top:8px">A change to your pickup information will appear here. You can always check the latest estimate.</p></div>'}</section>`;
}
function contactPanel(trip) {
  const key = keyFor('contact'); const draft = drafts.get(key);
  const requests = state.requests.filter(r => r.tripId === trip.id);
  const latest = requests.at(-1);
  return `<section class="card contact-card" aria-labelledby="contact-heading"><h2 id="contact-heading">Need a different plan?</h2><p>If the revised time will not work, let dispatch know. This does not change your ride automatically.</p><form id="contact-form" data-draft="${key}" data-revision="${draft?.revision ?? state.revision}" novalidate>${staleHint(key)}<div class="field"><label for="contact-message">Message to dispatch</label><textarea id="contact-message" name="message" rows="3" maxlength="500" aria-describedby="contact-hint contact-error">${escape(draft?.values.message ?? '')}</textarea><small id="contact-hint">1–500 characters · for your ${trip.direction.toLowerCase()} trip</small><div id="contact-error" class="field-error"></div></div><button type="submit" class="primary" id="contact-submit">Send demo request</button></form>${latest ? `<div class="request-receipt"><strong>${latest.reviewed ? 'Reviewed by dispatch' : 'Demo request received'} · ${latest.id}</strong><br>Sent at ${formatTime(latest.createdAt)} · ETA snapshot ${formatTime(latest.eta)}.<br>No schedule change has been approved.</div>` : ''}</section>`;
}
function dispatchEditor(trip) {
  const key = keyFor('editor'); const draft = drafts.get(key);
  const values = draft?.values ?? { eta: timeInput(trip.eta), status: trip.status, acceptedChange: false };
  const clockDraft = drafts.get('clock'); const channelDraft = drafts.get('channel');
  return `<section class="card" aria-labelledby="edit-heading"><p class="eyebrow">${trip.direction.toUpperCase()} TRIP</p><h2 id="edit-heading">Update pickup information</h2><p class="small">Original window <strong>${windowLabel(trip)}</strong> stays fixed.</p><form id="trip-form" data-draft="${key}" data-revision="${draft?.revision ?? state.revision}" novalidate>${staleHint(key)}<div class="field"><label for="edit-eta">Estimated arrival · Eastern</label><input type="time" id="edit-eta" name="eta" value="${escape(values.eta)}" aria-describedby="eta-hint trip-error"><small id="eta-hint">Leave blank if no estimate is available.</small></div><div class="field"><label for="edit-status">Vehicle status</label><select id="edit-status" name="status">${['scheduled','en-route','arrived','completed'].map(s => `<option value="${s}" ${values.status === s ? 'selected' : ''}>${statusLabel(s)}</option>`).join('')}</select></div><label class="check-row" for="driver-accepted"><input type="checkbox" id="driver-accepted" name="acceptedChange" ${values.acceptedChange ? 'checked' : ''}><span>Driver accepted this pickup-information change <span class="small">(simulated)</span></span></label><p class="small">A predicted delay triggers its own notice, even without driver acceptance.</p><div id="trip-error" class="field-error"></div><div class="button-row"><button id="save-trip" class="primary" type="submit">Save pickup update</button><button id="send-change" type="button" data-change ${viewRevision()}>Send change notice</button></div></form><hr class="subtle-rule"><form id="clock-form" data-draft="clock" data-revision="${clockDraft?.revision ?? state.revision}" novalidate>${staleHint('clock')}<div class="field"><label for="demo-time">Demo service time · Eastern</label><input id="demo-time" name="now" type="time" value="${clockDraft?.values.now ?? timeInput(state.now)}" aria-describedby="clock-hint clock-error"><small id="clock-hint">Move forward to test when a delay is identified.</small><div id="clock-error" class="field-error"></div></div><button id="set-clock" type="submit">Set demo time</button></form><hr class="subtle-rule"><form id="channel-form" data-draft="channel" data-revision="${channelDraft?.revision ?? state.revision}">${staleHint('channel')}<div class="field"><label for="channel">Rider's preferred channel</label><select id="channel" name="channel">${['sms','phone','email'].map(c => `<option value="${c}" ${(channelDraft?.values.channel ?? state.channel) === c ? 'selected' : ''}>${channelLabel(c)} (simulated)</option>`).join('')}</select></div><button id="save-channel" type="submit">Save channel preference</button></form></section>`;
}
function dispatchCommunications() {
  const notices = state.notices.toReversed();
  return `<section class="card" aria-labelledby="communications-heading"><div class="card-header"><h2 id="communications-heading">Communication record</h2><span class="section-count">${notices.length}</span></div><p class="small">Delivery outcomes below are explicitly simulated. Sending is not proof that the rider received a message.</p>${notices.length ? notices.map(n => {
    const a = n.attempts.at(-1);
    let actions = a.outcome === 'sent' ? `<button id="deliver-${n.id}" data-outcome="delivered" data-notice="${n.id}" ${viewRevision()}>Mark delivered</button><button id="unreachable-${n.id}" data-outcome="unreachable" data-notice="${n.id}" ${viewRevision()}>Mark unreachable</button>` : a.outcome === 'delivered' ? `<button id="external-ack-${n.id}" data-outcome="acknowledged" data-notice="${n.id}" ${viewRevision()}>Record external acknowledgement</button>` : a.outcome === 'unreachable' ? `<button id="retry-${n.id}" data-retry="${n.id}" ${viewRevision()}>Retry on ${channelLabel(state.channel)}</button>` : '';
    return `<article class="queue-item"><div class="notice-meta"><span class="trip-id">${n.id} · ${n.tripId === 'return' ? 'Return' : 'Outbound'}</span><span class="pill ${a.outcome}">${a.outcome}</span></div><p class="small">${n.kind === 'delay' ? 'Identified' : 'Created'} ${formatTime(n.createdAt)}</p><h3 style="margin-top:12px">${noticeTitle(n)}</h3>${noticeBody(n)}${attemptHistory(n)}<div class="button-row">${actions}</div></article>`;
  }).join('') : '<div class="empty">No communication events yet. Save a delayed estimate or send an accepted-change notice.</div>'}</section>`;
}
function dispatchRequests() {
  return `<section class="card" aria-labelledby="requests-heading"><div class="card-header"><h2 id="requests-heading">Rider requests</h2><span class="section-count">${state.requests.filter(r => !r.reviewed).length} open</span></div>${state.requests.length ? state.requests.toReversed().map(r => `<article class="queue-item"><div class="notice-meta"><span class="trip-id">${r.id} · ${r.tripId === 'return' ? 'Return' : 'Outbound'}</span><span class="pill">${r.reviewed ? 'Reviewed' : 'Needs review'}</span></div><p class="message" style="margin-top:12px">${escape(r.message)}</p><p class="small">Submitted ${formatTime(r.createdAt)} · ETA snapshot ${formatTime(r.eta)}.<br>Review does not approve or apply a new schedule.</p>${r.reviewed ? `<p class="small">Reviewed ${formatTime(r.reviewedAt)}</p>` : `<button id="review-${r.id}" data-review="${r.id}" ${viewRevision()}>Mark reviewed</button>`}</article>`).join('') : '<div class="empty">No rider requests yet.</div>'}</section>`;
}

function render() {
  const focus = captureFocus();
  const trip = state.trips.find(t => t.id === selected);
  $('page-title').textContent = view === 'rider' ? 'Your rides today' : 'Keep riders informed';
  $('page-intro').textContent = view === 'rider' ? 'Know your pickup time. Stay informed if it changes.' : 'One trip record. Clear updates. A visible communication trail.';
  $('view-rider').setAttribute('aria-pressed', String(view === 'rider'));
  $('view-dispatch').setAttribute('aria-pressed', String(view === 'dispatch'));
  $('clock-display').textContent = formatTime(state.now);
  $('storage-warning').hidden = store.mode !== 'temporary';
  $('storage-warning').textContent = store.warning;
  $('session-status').textContent = store.mode === 'shared' ? `Same-browser shared demo · revision ${state.revision}` : 'Temporary current-tab demo · not shared';
  renderLegs();
  $('content').innerHTML = view === 'rider' ? `<div class="rider-layout">${tripPanel(trip)}<div class="side-stack">${riderNotices()}${contactPanel(trip)}</div></div>` : `<div class="dispatch-layout">${dispatchEditor(trip)}<div class="dispatch-stack">${dispatchCommunications()}${dispatchRequests()}</div></div>`;
  restoreFocus(focus);
}
store.subscribe(next => {
  state = next; render();
  if (!busy) announce('Trip information updated in another view. Review any unsaved form before saving.');
});

async function run(cmd, revision, message, { draftKey, errorId, inputId } = {}) {
  if (busy) return;
  busy = true;
  try {
    state = await store.commit(revision, cmd);
    if (draftKey) drafts.delete(draftKey);
    render();
    if (errorId && $(errorId)) $(errorId).textContent = '';
    if (inputId && $(inputId)) $(inputId).removeAttribute('aria-invalid');
    announce(`${message}${store.mode === 'temporary' ? ' Temporary only; this change is not saved across tabs.' : ''}`);
  } catch (error) {
    state = store.read(); render();
    if (errorId && $(errorId)) $(errorId).textContent = error.message;
    if (inputId && $(inputId)) { $(inputId).setAttribute('aria-invalid', 'true'); $(inputId).focus(); }
    announce(error.message, true);
  } finally { busy = false; }
}

document.addEventListener('input', event => {
  const form = event.target.closest('form[data-draft]'); if (!form) return;
  const data = new FormData(form); const values = Object.fromEntries(data);
  if (form.id === 'trip-form') values.acceptedChange = data.has('acceptedChange');
  drafts.set(form.dataset.draft, { revision: Number(form.dataset.revision), values });
});
document.addEventListener('change', event => {
  const form = event.target.closest('form[data-draft]');
  if (form) form.dispatchEvent(new Event('input', { bubbles: true }));
});
document.addEventListener('click', event => {
  const button = event.target.closest('button'); if (!button || button.getAttribute('aria-disabled') === 'true') return;
  if (button.dataset.view) { view = button.dataset.view; rememberView(); render(); return; }
  if (button.dataset.leg) { selected = button.dataset.leg; rememberView(); render(); return; }
  if (button.dataset.refresh) { drafts.delete(button.dataset.refresh); render(); announce('Form refreshed with the latest demo values.'); return; }
  const revision = Number(button.dataset.revision ?? state.revision);
  if (button.dataset.scenario) {
    selected = button.dataset.scenario === 'normal' ? 'outbound' : 'return'; drafts.clear(); rememberView();
    run({ type: 'loadScenario', scenario: button.dataset.scenario }, state.revision, 'Sample scenario loaded. Previous fictional records were replaced.');
  } else if (button.dataset.outcome) {
    run({ type: 'setOutcome', noticeId: button.dataset.notice, outcome: button.dataset.outcome }, revision, `Simulated notice outcome recorded: ${button.dataset.outcome}.`);
  } else if (button.dataset.retry) {
    run({ type: 'retryNotice', noticeId: button.dataset.retry }, revision, 'New simulated send attempt recorded. Previous attempt remains in history.');
  } else if (button.dataset.review) {
    run({ type: 'reviewRequest', requestId: button.dataset.review }, revision, 'Request marked reviewed. The trip schedule is unchanged.');
  } else if (button.hasAttribute('data-change')) {
    const form = $('trip-form');
    run({ type: 'sendChange', tripId: selected, accepted: $('driver-accepted').checked }, Number(form.dataset.revision), 'Accepted-change notice created on the simulated channel.', { errorId: 'trip-error' });
  }
});
document.addEventListener('submit', event => {
  const form = event.target; if (!form.matches('form')) return;
  event.preventDefault();
  const data = new FormData(form); const revision = Number(form.dataset.revision);
  const options = { draftKey: form.dataset.draft };
  try {
    if (form.id === 'contact-form') {
      run({ type: 'contact', tripId: selected, message: data.get('message') }, revision, 'Demo request received. Dispatch can review it; your schedule has not changed.', { ...options, errorId: 'contact-error', inputId: 'contact-message' });
    } else if (form.id === 'trip-form') {
      run({ type: 'updateTrip', tripId: selected, eta: parseTime(data.get('eta')), status: data.get('status'), acceptedChange: data.has('acceptedChange') }, revision, 'Pickup information saved. Any new notice is visible in the communication record.', { ...options, errorId: 'trip-error', inputId: 'edit-eta' });
    } else if (form.id === 'clock-form') {
      run({ type: 'setClock', now: parseTime(data.get('now')) }, revision, 'Demo service time updated.', { ...options, errorId: 'clock-error', inputId: 'demo-time' });
    } else if (form.id === 'channel-form') {
      run({ type: 'setChannel', channel: data.get('channel') }, revision, 'Preference saved for future simulated notices and retries.', options);
    }
  } catch (error) {
    const id = form.id === 'trip-form' ? 'trip-error' : 'clock-error';
    if ($(id)) $(id).textContent = error.message;
    announce(error.message, true);
  }
});
render();
