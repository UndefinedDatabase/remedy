import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import FactCheckOutlinedIcon from "@mui/icons-material/FactCheckOutlined";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import MemoryIcon from "@mui/icons-material/Memory";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import styles from "./LayerSwitcher.module.css";

const layers = [["Journey", AutoAwesomeIcon], ["Proof", FactCheckOutlinedIcon], ["Files", FolderOutlinedIcon], ["Memory", MemoryIcon], ["Diagnostics", SettingsOutlinedIcon]] as const;

export function LayerSwitcher() {
  return (
    <nav className={`${styles.switcher} remedy-layer-switcher`} aria-label="View layers" data-ui="layer-switcher">
      {layers.map(([label, Icon], i) => (
        <button key={label} type="button" className={i === 0 ? styles.active : styles.button} aria-label={label}>
          <Icon fontSize="small" />
        </button>
      ))}
    </nav>
  );
}
