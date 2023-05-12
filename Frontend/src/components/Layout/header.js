import classes from "./header.module.css";
import Link from "next/link";

function Header() {
  return (
    <header className={classes.header}>
      <div className={classes.logo}>
        <Link href="/">Weather Details and Stats</Link>
      </div>
      {/* <nav>
        <ul>
          <li>
            <Link href="/summary">Summary</Link>
          </li>
        </ul>
      </nav> */}
    </header>
  );
}

export default Header;
