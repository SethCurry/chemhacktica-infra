import { Link } from "react-router";
import { doMakeRestart } from "../api";

export default function NavBar() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        width: "100%",
        height: "2rem",
        backgroundColor: "black",
        color: "white",
        gap: "1rem",
      }}
    >
      <Link to="/">
        <img
          src="/favicon.ico"
          alt="ChemInfra"
          style={{ height: "100%", width: "auto" }}
        />
      </Link>
      <span style={{ flexGrow: 1 }} />
      <button
        style={{
          backgroundColor: "white",
          color: "black",
          borderRadius: "0.5em",
          margin: "0.25rem",
        }}
        onClick={() => doMakeRestart()}
      >
        Restart
      </button>
    </div>
  );
}
