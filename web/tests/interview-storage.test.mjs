import assert from 'node:assert/strict';

const {
  INTERVIEW_STORAGE_KEY,
  answeredCount,
  clearInterviewState,
  emptyInterviewState,
  exportInterviewJson,
  loadInterviewState,
  normalizeInterviewState,
  saveInterviewState,
  skipQuestion,
  updateAnswer,
} = await import('../src/lib/interview.ts');

const values = new Map();
const storage = {
  getItem(key) {
    return values.get(key) ?? null;
  },
  setItem(key, value) {
    values.set(key, value);
  },
  removeItem(key) {
    values.delete(key);
  },
};

let state = emptyInterviewState();
state = updateAnswer(state, 'curiosity', '시스템이 실패하는 방식', 1);
assert.equal(answeredCount(state), 1);
assert.equal(saveInterviewState(state, storage), true);
assert.equal(values.has(INTERVIEW_STORAGE_KEY), true);

const loaded = loadInterviewState(storage);
assert.equal(loaded.persisted, true);
assert.equal(loaded.state.answers.curiosity, '시스템이 실패하는 방식');

state = skipQuestion(loaded.state, 'evidence', 2);
assert.deepEqual(state.skipped, ['evidence']);
state = updateAnswer(state, 'evidence', '새 상황에 적용한다', 2);
assert.deepEqual(state.skipped, []);
assert.equal(answeredCount(state), 2);

const malformed = normalizeInterviewState({
  currentIndex: -4,
  answers: { safe: 'value', ignored: 42 },
  skipped: ['later', 3],
});
assert.equal(malformed.currentIndex, 0);
assert.deepEqual(malformed.answers, { safe: 'value' });
assert.deepEqual(malformed.skipped, ['later']);
assert.match(exportInterviewJson(state), /새 상황에 적용한다/);

assert.equal(clearInterviewState(storage), true);
assert.equal(values.has(INTERVIEW_STORAGE_KEY), false);

const blockedStorage = {
  getItem() {
    throw new Error('blocked');
  },
  setItem() {
    throw new Error('blocked');
  },
  removeItem() {
    throw new Error('blocked');
  },
};
assert.equal(loadInterviewState(blockedStorage).persisted, false);
assert.equal(saveInterviewState(state, blockedStorage), false);
assert.equal(clearInterviewState(blockedStorage), false);

console.log('interview storage tests passed');
