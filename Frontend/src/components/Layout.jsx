import React, {useState, useEffect, useRef} from "react"
import { Outlet, NavLink } from "react-router-dom"

import Logo from '../assets/logo_bez_tla.png';

import '../styles/Global.css'
import '../styles/Navbar.css'


function Layout() {
  const [isOpen, setIsOpen] = useState(false);
  const isSuperUser = localStorage.getItem("IS_SUPERUSER") === "true";

  const navBurgerRef = useRef(null);
  const iconBurgerRef = useRef(null);

  

  const handleToggleClick = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isOpen &&
        navBurgerRef.current &&
        !navBurgerRef.current.contains(event.target) &&
        iconBurgerRef.current &&
        !iconBurgerRef.current.contains(event.target)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <>
      <nav className="navbar">
        <div className="logo-navbar">
          <img src={Logo} alt="SaveSpace logo" />
          <span>SaveSpace</span>
        </div>
        <ul className="nav-links">
          <li><NavLink to="/">strona główna</NavLink></li>
          <li><NavLink to="/categories">kategorie</NavLink></li>
          <li><NavLink to="/summary">podsumowanie</NavLink></li>
          <li><NavLink to="/settings">ustawienia</NavLink></li>
          {isSuperUser && <li><NavLink to="/admin">admin</NavLink></li>}
        </ul>
        <div className="iconBurger" id="iconBurger" onClick={handleToggleClick} ref={iconBurgerRef}>
          <svg width="40" height="35" viewBox="0 0 22 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="m0.78125 3.51562h20.3125c0.4315 0 0.78125-0.349756 0.78125-0.78125v-1.95312c0-0.431494-0.34975-0.78125-0.78125-0.78125h-20.3125c-0.431494 0-0.78125 0.349756-0.78125 0.78125v1.95312c0 0.431494 0.349756 0.78125 0.78125 0.78125zm0 7.81248h20.3125c0.4315 0 0.78125-0.349756 0.78125-0.78125v-1.95312c0-0.431494-0.34975-0.78125-0.78125-0.78125h-20.3125c-0.431494 0-0.78125 0.349756-0.78125 0.78125v1.95312c0 0.431494 0.349756 0.78125 0.78125 0.78125zm0 7.81248h20.3125c0.4315 0 0.78125-0.349756 0.78125-0.78125v-1.95312c0-0.431494-0.34975-0.78125-0.78125-0.78125h-20.3125c-0.431494 0-0.78125 0.349756-0.78125 0.78125v1.95312c0 0.431494 0.349756 0.78125 0.78125 0.78125z" fill="black"/>
          </svg>
        </div>
      </nav>

      <div className={`navBurger ${isOpen ? 'active' : ''}`} id="navBurger" ref={navBurgerRef}>
        <ul>
          <li><NavLink to="/">strona główna</NavLink></li>
          <li><NavLink to="/categories">kategorie</NavLink></li>
          <li><NavLink to="/summary">podsumowanie</NavLink></li>
          <li><NavLink to="/settings">ustawienia</NavLink></li>
          {isSuperUser && <li><NavLink to="/admin">admin</NavLink></li>}
        </ul>
    </div>

      <main className="content">
        <Outlet />
      </main>
    </>
  )
}

export default Layout
