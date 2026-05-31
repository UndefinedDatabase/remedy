import React from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import RemedyApp from "./RemedyApp";
import "./styles/globals.css";

const theme = createTheme({
  palette: { mode: "light", primary: { main: "#4c83ff" }, text: { primary: "#14254b", secondary: "#6e7fa3" }, background: { default: "#edf3fb" } },
  shape: { borderRadius: 18 },
  typography: { fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' },
});

createRoot(document.getElementById("root")!).render(
  <React.StrictMode><ThemeProvider theme={theme}><RemedyApp /></ThemeProvider></React.StrictMode>
);
