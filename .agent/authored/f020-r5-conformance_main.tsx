// F020 T003 conformance harness page: paints the kind-by-state matrix fixture
// (apps/ui/src/components/graph/renderers/glyphMatrix.ts) with the live
// painter on a real canvas at CONFORMANCE_SCALE, reads the pixel under every
// probe glyphConformance.ts places, and judges each with the same judgeProbe
// its unit tests pin. The page invents no geometry, colour or rule of its own.
import "../../apps/ui/src/styles/tokens.css";
import { glyphMatrixSize, paintGlyphMatrix } from "../../apps/ui/src/components/graph/renderers/glyphMatrix";
import { CONFORMANCE_SCALE, conformanceProbes, judgeProbe } from "../../apps/ui/src/components/graph/renderers/glyphConformance";
import { readDocumentPalette } from "../../apps/ui/src/components/graph/renderers/palette";

interface ConformanceResult {
  total: number;
  passed: number;
  missing: string[];
  failures: string[];
  byMark: Record<string, { present: number; absent: number }>;
}

const { palette, missing } = readDocumentPalette();
const size = glyphMatrixSize();
const canvas = document.createElement("canvas");
canvas.width = size.width * CONFORMANCE_SCALE;
canvas.height = size.height * CONFORMANCE_SCALE;
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d", { willReadFrequently: true }) as CanvasRenderingContext2D;
ctx.scale(CONFORMANCE_SCALE, CONFORMANCE_SCALE);
paintGlyphMatrix(ctx, palette);

const probes = conformanceProbes(CONFORMANCE_SCALE);
const failures: string[] = [];
const byMark: Record<string, { present: number; absent: number }> = {};
let passed = 0;
for (const probe of probes) {
  const [r, g, b, a] = ctx.getImageData(Math.floor(probe.x), Math.floor(probe.y), 1, 1).data;
  const verdict = judgeProbe(probe, { r, g, b, a }, palette);
  const key = `${probe.mark}/${probe.part}`;
  byMark[key] = byMark[key] ?? { present: 0, absent: 0 };
  if (verdict.ok) {
    passed += 1;
    byMark[key][probe.expect] += 1;
  } else {
    failures.push(`${probe.kind}/${probe.state} ${key}: ${verdict.why}`);
  }
}
const result: ConformanceResult = { total: probes.length, passed, missing, failures, byMark };
(window as unknown as { __conformance: ConformanceResult }).__conformance = result;
