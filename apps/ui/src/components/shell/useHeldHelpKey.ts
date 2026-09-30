// T5_F044 T002, DECISION F044 D6 — the held "?": a tap opens the terms panel, on the shell's own
// route; held past KEYMAP_HOLD_MS it shows the keymap's own cheat overlay instead, until the key
// is let go. The timer lives HERE, not in RemedyShell.tsx, because
// tests/ui_contracts/test_timeline_scrub_wiring.py keeps every timer out of the shell; the
// shell's own key listener hands this hook every "?" the keymap reads as "open-terms".
import { useCallback, useEffect, useRef, useState } from "react";
import { KEYMAP_HOLD_MS } from "../../api/keymap";

/** What the shell reads back: whether the overlay is shown, and the press the shell's own
 *  listener hands every "?" it reads as "open-terms". */
export interface HeldHelpKey {
  readonly shortcutsOpen: boolean;
  press(repeat: boolean): void;
}

export function useHeldHelpKey(onTap: () => void): HeldHelpKey {
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const openRef = useRef(false);
  const pending = useRef<number | null>(null);
  const onTapRef = useRef(onTap);
  onTapRef.current = onTap;

  const press = useCallback((repeat: boolean) => {
    if (repeat || pending.current !== null || openRef.current) return;
    pending.current = window.setTimeout(() => {
      pending.current = null;
      openRef.current = true;
      setShortcutsOpen(true);
    }, KEYMAP_HOLD_MS);
  }, []);

  useEffect(() => {
    const onKeyUp = (event: KeyboardEvent) => {
      if (event.key !== "?" && event.key !== "/") return;
      if (pending.current !== null) {
        window.clearTimeout(pending.current);
        pending.current = null;
        onTapRef.current();
      } else if (openRef.current) {
        openRef.current = false;
        setShortcutsOpen(false);
      }
    };
    const onBlur = () => {
      if (pending.current !== null) {
        window.clearTimeout(pending.current);
        pending.current = null;
      }
      openRef.current = false;
      setShortcutsOpen(false);
    };
    window.addEventListener("keyup", onKeyUp);
    window.addEventListener("blur", onBlur);
    return () => {
      window.removeEventListener("keyup", onKeyUp);
      window.removeEventListener("blur", onBlur);
      if (pending.current !== null) window.clearTimeout(pending.current);
    };
  }, []);

  return { shortcutsOpen, press };
}
