import assert from 'node:assert/strict';

globalThis.localStorage = {
  getItem() {
    return null;
  },
  setItem() {
    throw new Error('storage quota denied');
  },
};

const { localProgressAdapter } = await import('../src/lib/progress.ts');
const lessonId = 'lesson-storage-failure';

const mutation = localProgressAdapter.setStage(
  lessonId,
  'explanation',
  true,
);
assert.equal(mutation.persisted, false);
assert.deepEqual(mutation.progress.completedStages, ['explanation']);

const reread = localProgressAdapter.read(lessonId);
assert.equal(reread.persisted, false);
assert.deepEqual(reread.progress.completedStages, ['explanation']);

console.log('progress storage fallback test passed');
