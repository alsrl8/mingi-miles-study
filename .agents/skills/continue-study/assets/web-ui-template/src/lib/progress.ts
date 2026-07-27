export const LOCAL_PROGRESS_STORAGE_KEY = 'mingi-study-navigation-progress-v1';

export const lessonStageDescriptors = [
  { id: 'explanation', label: '개념' },
  { id: 'worked-example', label: '예제' },
  { id: 'guided-task', label: 'Guided' },
  { id: 'independent-task', label: '독립 과제' },
  { id: 'assessment', label: '시험' },
] as const;

export const lessonStages = lessonStageDescriptors.map((stage) => stage.id);

export type LessonStage = (typeof lessonStageDescriptors)[number]['id'];

export type LessonProgress = {
  lessonId: string;
  completedStages: LessonStage[];
  updatedAt: string;
};

type ProgressEnvelope = {
  version: 1;
  lessons: Record<string, LessonProgress>;
};

export type ProgressResult = {
  progress: LessonProgress;
  persisted: boolean;
};

export interface NavigationProgressAdapter {
  read(lessonId: string): ProgressResult;
  setStage(
    lessonId: string,
    stage: LessonStage,
    complete: boolean,
  ): ProgressResult;
  reset(lessonId: string): ProgressResult;
}

let memoryEnvelope: ProgressEnvelope = { version: 1, lessons: {} };
let hasUnsavedMemory = false;

export function isLessonStage(value: string | undefined): value is LessonStage {
  return lessonStageDescriptors.some((stage) => stage.id === value);
}

export function emptyProgress(lessonId: string): LessonProgress {
  return {
    lessonId,
    completedStages: [],
    updatedAt: new Date(0).toISOString(),
  };
}

function normalizeProgress(
  lessonId: string,
  candidate: unknown,
): LessonProgress {
  if (!candidate || typeof candidate !== 'object') {
    return emptyProgress(lessonId);
  }

  const value = candidate as Partial<LessonProgress>;
  return {
    lessonId,
    completedStages: Array.isArray(value.completedStages)
      ? value.completedStages.filter(
          (stage): stage is LessonStage =>
            typeof stage === 'string' && isLessonStage(stage),
        )
      : [],
    updatedAt:
      typeof value.updatedAt === 'string'
        ? value.updatedAt
        : new Date(0).toISOString(),
  };
}

function readEnvelope(): { envelope: ProgressEnvelope; persisted: boolean } {
  if (typeof localStorage === 'undefined') {
    return { envelope: memoryEnvelope, persisted: false };
  }
  if (hasUnsavedMemory) {
    return { envelope: memoryEnvelope, persisted: false };
  }

  try {
    const raw = localStorage.getItem(LOCAL_PROGRESS_STORAGE_KEY);
    if (!raw) {
      return { envelope: memoryEnvelope, persisted: true };
    }

    const parsed = JSON.parse(raw) as Partial<ProgressEnvelope>;
    if (
      parsed.version !== 1 ||
      !parsed.lessons ||
      typeof parsed.lessons !== 'object'
    ) {
      return { envelope: memoryEnvelope, persisted: false };
    }

    const lessons = Object.fromEntries(
      Object.entries(parsed.lessons).map(([lessonId, progress]) => [
        lessonId,
        normalizeProgress(lessonId, progress),
      ]),
    );
    memoryEnvelope = { version: 1, lessons };
    hasUnsavedMemory = false;
    return { envelope: memoryEnvelope, persisted: true };
  } catch {
    return { envelope: memoryEnvelope, persisted: false };
  }
}

function writeEnvelope(envelope: ProgressEnvelope): boolean {
  memoryEnvelope = envelope;
  if (typeof localStorage === 'undefined') return false;

  try {
    localStorage.setItem(LOCAL_PROGRESS_STORAGE_KEY, JSON.stringify(envelope));
    hasUnsavedMemory = false;
    return true;
  } catch {
    hasUnsavedMemory = true;
    return false;
  }
}

export const localProgressAdapter: NavigationProgressAdapter = {
  read(lessonId) {
    const { envelope, persisted } = readEnvelope();
    return {
      progress: normalizeProgress(lessonId, envelope.lessons[lessonId]),
      persisted,
    };
  },

  setStage(lessonId, stage, complete) {
    const { envelope } = readEnvelope();
    const current = normalizeProgress(lessonId, envelope.lessons[lessonId]);
    const completedStages = new Set(current.completedStages);

    if (complete) completedStages.add(stage);
    else completedStages.delete(stage);

    const progress = {
      lessonId,
      completedStages: [...completedStages],
      updatedAt: new Date().toISOString(),
    };
    const persisted = writeEnvelope({
      version: 1,
      lessons: { ...envelope.lessons, [lessonId]: progress },
    });
    return { progress, persisted };
  },

  reset(lessonId) {
    const { envelope } = readEnvelope();
    const progress = emptyProgress(lessonId);
    const persisted = writeEnvelope({
      version: 1,
      lessons: { ...envelope.lessons, [lessonId]: progress },
    });
    return { progress, persisted };
  },
};
