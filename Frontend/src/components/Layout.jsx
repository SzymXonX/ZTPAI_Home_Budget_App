// components/Layout.jsx
import React from "react"
import { Outlet, NavLink } from "react-router-dom"

import Logo from '../assets/logo.png';

import '../styles/Global.css'
import '../styles/Navbar.css'


function Layout() {
    const isSuperUser = localStorage.getItem("IS_SUPERUSER") === "true";
  return (
    <>
      <nav className="navbar">
        <div className="logo">
          <img src={Logo} alt="SaveSpace logo" />
          <span>SaveSpace</span>
        </div>
        <ul className="nav-links">
          <li><NavLink to="/main">strona główna</NavLink></li>
          <li><NavLink to="/categories">kategorie</NavLink></li>
          <li><NavLink to="/summary">podsumowanie</NavLink></li>
          <li><NavLink to="/settings">ustawienia</NavLink></li>
          {isSuperUser && <li><NavLink to="/admin">admin</NavLink></li>}
        </ul>
      </nav>

      {/* Tu wstawiany jest content aktualnej strony */}
      <main class="content">
        <Outlet />
      </main>
    </>
  )
}

export default Layout
