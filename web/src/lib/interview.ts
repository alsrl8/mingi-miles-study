export const INTERVIEW_STORAGE_KEY = 'miles-learner-interview-v1';

export type InterviewState = {
  version: 1;
  currentIndex: number;
  answers: Record<string, string>;
  skipped: string[];
  updatedAt: string;
  completedAt?: string;
};

export function emptyInterviewState(): InterviewState {
  return {
    version: 1,
    currentIndex: 0,
    answers: {},
    skipped: [],
    updatedAt: new Date(0).toISOString(),
  };
}

export function normalizeInterviewState(candidate: unknown): InterviewState {
  if (!candidate || typeof candidate !== 'object') return emptyInterviewState();

  const value = candidate as Partial<InterviewState>;
  const answers =
    value.answers && typeof value.answers === 'object'
      ? Object.fromEntries(
          Object.entries(value.answers).filter(
            ([key, answer]) =>
              typeof key === 'string' && typeof answer === 'string',
          ),
        )
      : {};

  return {
    version: 1,
    currentIndex:
      Number.isInteger(value.currentIndex) && Number(value.currentIndex) >= 0
        ? Number(value.currentIndex)
        : 0,
    answers,
    skipped: Array.isArray(value.skipped)
      ? value.skipped.filter((id): id is string => typeof id === 'string')
      : [],
    updatedAt:
      typeof value.updatedAt === 'string'
        ? value.updatedAt
        : new Date(0).toISOString(),
    ...(typeof value.completedAt === 'string'
      ? { completedAt: value.completedAt }
      : {}),
  };
}

export function loadInterviewState(
  storage: Pick<Storage, 'getItem'> | undefined = globalThis.localStorage,
): { state: InterviewState; persisted: boolean } {
  if (!storage) return { state: emptyInterviewState(), persisted: false };

  try {
    const raw = storage.getItem(INTERVIEW_STORAGE_KEY);
    return {
      state: raw
        ? normalizeInterviewState(JSON.parse(raw))
        : emptyInterviewState(),
      persisted: true,
    };
  } catch {
    return { state: emptyInterviewState(), persisted: false };
  }
}

export function saveInterviewState(
  state: InterviewState,
  storage: Pick<Storage, 'setItem'> | undefined = globalThis.localStorage,
): boolean {
  if (!storage) return false;

  try {
    storage.setItem(INTERVIEW_STORAGE_KEY, JSON.stringify(state));
    return true;
  } catch {
    return false;
  }
}

export function clearInterviewState(
  storage: Pick<Storage, 'removeItem'> | undefined = globalThis.localStorage,
): boolean {
  if (!storage) return false;

  try {
    storage.removeItem(INTERVIEW_STORAGE_KEY);
    return true;
  } catch {
    return false;
  }
}

export function answeredCount(state: InterviewState): number {
  return Object.values(state.answers).filter((answer) => answer.trim()).length;
}

export function updateAnswer(
  state: InterviewState,
  questionId: string,
  answer: string,
  currentIndex: number,
): InterviewState {
  const skipped = state.skipped.filter((id) => id !== questionId);
  const answers = { ...state.answers };
  if (answer.trim()) answers[questionId] = answer;
  else delete answers[questionId];

  return {
    ...state,
    currentIndex,
    answers,
    skipped,
    updatedAt: new Date().toISOString(),
  };
}

export function skipQuestion(
  state: InterviewState,
  questionId: string,
  currentIndex: number,
): InterviewState {
  const answers = { ...state.answers };
  delete answers[questionId];
  return {
    ...state,
    currentIndex,
    answers,
    skipped: [...new Set([...state.skipped, questionId])],
    updatedAt: new Date().toISOString(),
  };
}

export function exportInterviewJson(state: InterviewState): string {
  return JSON.stringify(state, null, 2);
}
