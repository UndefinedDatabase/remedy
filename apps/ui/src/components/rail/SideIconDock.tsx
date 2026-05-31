import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import HistoryIcon from "@mui/icons-material/History";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import ShowChartIcon from "@mui/icons-material/ShowChart";
import styles from "./SideIconDock.module.css";

const items = [["Overview", AutoAwesomeIcon], ["Checks", CheckCircleOutlineIcon], ["Activity", ShowChartIcon], ["Files", FolderOutlinedIcon], ["History", HistoryIcon], ["Docs", MenuBookOutlinedIcon], ["Settings", SettingsOutlinedIcon]] as const;

export function SideIconDock({ className }: { className?: string }) {
  return (
    <nav className={`${styles.dock} ${className || ""}`} aria-label="Remedy sections">
      {items.map(([label, Icon], i) => (
        <button key={label} className={i === 0 ? styles.active : styles.button} aria-label={label}>
          <Icon fontSize="small" />
        </button>
      ))}
    </nav>
  );
}
