import { createInitialState, applyCommand } from './domain.js';
export const STORAGE_KEY = 'rideclear:a3:v2:state';
const LOCK_NAME = 'rideclear-a3-v2-state';
const clone = x => structuredClone(x);
function browserStorage() { try { return globalThis.localStorage; } catch { return null; } }
function parse(raw) {
  const state = JSON.parse(raw);
  if (state.schemaVersion !== 1 || !Number.isInteger(state.revision) || !Array.isArray(state.trips)
      || state.trips.length !== 2 || !Array.isArray(state.notices) || !Array.isArray(state.requests)) {
    throw new Error('Unsupported demo state');
  }
  return state;
}
export function createStore(options = {}) {
  const storage = Object.hasOwn(options, 'storage') ? options.storage : browserStorage();
  const locks = Object.hasOwn(options, 'locks') ? options.locks : globalThis.navigator?.locks;
  const listeners = new Set();
  let current = createInitialState();
  let durable = Boolean(storage && locks?.request);
  let warning = durable ? '' : 'Temporary demo in the current tab only. Saving and cross-tab sharing are unavailable.';
  if (storage) {
    try { const raw = storage.getItem(STORAGE_KEY); if (raw) current = parse(raw); }
    catch { durable = false; warning = 'Saved demo data cannot be read. This is a temporary, single-tab session.'; }
  }
  const emit = () => { for (const listener of listeners) listener(clone(current)); };
  const onExternal = event => {
    if (!durable || event.key !== STORAGE_KEY) return;
    try {
      const raw = storage.getItem(STORAGE_KEY);
      if (raw) { current = parse(raw); emit(); }
    } catch { durable = false; warning = 'Demo sharing is unavailable. Changes in this tab are temporary and not saved.'; emit(); }
  };
  globalThis.addEventListener?.('storage', onExternal);
  async function commit(expectedRevision, cmd) {
    const execute = () => {
      if (durable) {
        try { const raw = storage.getItem(STORAGE_KEY); if (raw) current = parse(raw); }
        catch { durable = false; warning = 'Demo storage cannot be read. Changes in this tab are temporary and not saved.'; }
      }
      if (expectedRevision !== current.revision) {
        emit(); const error = new Error('The data changed in another view. Review the latest values and try again.');
        error.code = 'STALE_REVISION'; throw error;
      }
      const next = applyCommand(current, cmd);
      if (next === current) return clone(current);
      next.revision = current.revision + 1;
      if (durable) {
        try { storage.setItem(STORAGE_KEY, JSON.stringify(next)); }
        catch { durable = false; warning = 'This change is not saved. Continue in this tab temporarily; reload may lose these changes.'; }
      }
      current = next; emit(); return clone(current);
    };
    return durable ? locks.request(LOCK_NAME, execute) : execute();
  }
  return {
    read: () => clone(current), commit,
    get mode() { return durable ? 'shared' : 'temporary'; },
    get warning() { return warning; },
    subscribe(listener) { listeners.add(listener); return () => listeners.delete(listener); },
    dispose() { globalThis.removeEventListener?.('storage', onExternal); listeners.clear(); }
  };
}
