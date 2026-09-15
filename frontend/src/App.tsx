import { useState } from "react";
import Header from "./components/Header";
import Checker from "./pages/Checker";
import Converter from "./pages/Converter";

type View = "check" | "convert";

export default function App() {
  const [view, setView] = useState<View>("check");

  return (
    <div className="min-h-screen bg-canvas">
      <Header view={view} onChange={setView} />
      {view === "check" ? <Checker /> : <Converter />}
    </div>
  );
}