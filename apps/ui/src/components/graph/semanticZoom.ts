export function semanticZoomLevelFromViewportZoom(zoom: number): number {
  if (zoom < 0.36) return 0;
  if (zoom < 0.62) return 1;
  if (zoom < 0.92) return 2;
  if (zoom < 1.28) return 3;
  return 4;
}
