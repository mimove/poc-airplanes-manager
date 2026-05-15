import { useState } from "react";
import HangarsPage from "./pages/HangarsPage";
import AirplanesPage from "./pages/AirplanesPage";
import FlightsPage from "./pages/FlightsPage";
import PassengersPage from "./pages/PassengersPage";

const TABS = ["Hangars", "Airplanes", "Flights", "Passengers"];
const PAGES = {
  Hangars: HangarsPage,
  Airplanes: AirplanesPage,
  Flights: FlightsPage,
  Passengers: PassengersPage,
};

export default function App() {
  const [tab, setTab] = useState("Hangars");
  const Page = PAGES[tab];
  return (
    <div className="app">
      <nav>
        <h1>Airplanes Manager</h1>
        <div className="tabs">
          {TABS.map((t) => (
            <button
              key={t}
              className={tab === t ? "active" : ""}
              onClick={() => setTab(t)}
            >
              {t}
            </button>
          ))}
        </div>
      </nav>
      <main>
        <Page />
      </main>
    </div>
  );
}
