import { localProgressAdapter } from './progress';

// Replace this single binding with an authenticated adapter after its
// authorization and failure behavior are tested.
export const progressAdapter = localProgressAdapter;
