import test from 'node:test';
import assert from 'node:assert/strict';
import { createStore, STORAGE_KEY } from '../frontend/store.js';

function memoryStorage() {
  const map = new Map(); return { getItem: k => map.get(k) ?? null, setItem: (k,v) => map.set(k,v) };
}
function serialLocks() {
  let tail = Promise.resolve();
  return { request: (_name, action) => { const next = tail.then(action); tail = next.catch(() => {}); return next; } };
}
test('durable state reloads and a stale editor cannot overwrite a newer revision', async () => {
  const storage = memoryStorage(); const locks = serialLocks();
  const a = createStore({ storage, locks }); const b = createStore({ storage, locks });
  const initial = a.read();
  const saved = await a.commit(initial.revision, { type: 'setChannel', channel: 'email' });
  assert.equal(saved.revision, initial.revision + 1);
  await assert.rejects(b.commit(initial.revision, { type: 'setChannel', channel: 'phone' }), /changed in another view/i);
  assert.equal(b.read().channel, 'email');
  const reloaded = createStore({ storage, locks }); assert.equal(reloaded.read().channel, 'email');
});
test('serialized same-revision concurrent writes cannot both succeed', async () => {
  const storage = memoryStorage(); const locks = serialLocks();
  const a = createStore({ storage, locks }); const b = createStore({ storage, locks });
  const results = await Promise.allSettled([
    a.commit(0, { type: 'setChannel', channel: 'email' }),
    b.commit(0, { type: 'setChannel', channel: 'phone' })
  ]);
  assert.equal(results.filter(x => x.status === 'fulfilled').length, 1);
  assert.equal(JSON.parse(storage.getItem(STORAGE_KEY)).revision, 1);
});
test('no-op does not bump revision; reset cannot restore a stale revision', async () => {
  const storage = memoryStorage(); const locks = serialLocks(); const store = createStore({ storage, locks });
  const unchanged = await store.commit(0, { type: 'setChannel', channel: 'sms' });
  assert.equal(unchanged.revision, 0);
  const changed = await store.commit(0, { type: 'setChannel', channel: 'email' });
  const reset = await store.commit(changed.revision, { type: 'reset' });
  assert.equal(reset.revision, 2); assert.equal(reset.channel, 'sms');
});
test('unavailable storage or locks is explicitly temporary, not cross-tab durable', async () => {
  const noLocks = createStore({ storage: memoryStorage(), locks: null });
  assert.equal(noLocks.mode, 'temporary'); assert.match(noLocks.warning, /single.tab|current tab/i);
  const denied = createStore({ storage: { getItem() { throw new Error('denied'); } }, locks: serialLocks() });
  assert.equal(denied.mode, 'temporary');
  const next = await denied.commit(0, { type: 'setChannel', channel: 'phone' });
  assert.equal(next.channel, 'phone');
});
test('failed durable write leaves saved data unchanged and labels temporary state', async () => {
  const storage = memoryStorage(); const locks = serialLocks(); const store = createStore({ storage, locks });
  await store.commit(0, { type: 'setChannel', channel: 'email' });
  const previous = storage.getItem(STORAGE_KEY);
  storage.setItem = () => { throw new Error('quota'); };
  const next = await store.commit(1, { type: 'setChannel', channel: 'phone' });
  assert.equal(next.channel, 'phone'); assert.equal(store.mode, 'temporary');
  assert.equal(storage.getItem(STORAGE_KEY), previous);
  assert.match(store.warning, /not saved|cannot save/i);
});
