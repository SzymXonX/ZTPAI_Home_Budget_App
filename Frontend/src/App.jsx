import React from "react"
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"

import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import Categories from "./pages/Categories"
import Summary from "./pages/Summary"
import Settings from "./pages/Settings"
import Admin from "./pages/Admin"
import NotFound from "./pages/NotFound"

import ProtectedRoute from "./components/ProtectedRoute"
import Layout from "./components/Layout"

function Logout() {
  localStorage.clear()
  localStorage.removeItem("IS_SUPERUSER")
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  localStorage.setItem("IS_SUPERUSER", "false")
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />

        <Route path="/" element={<ProtectedRoute> <Layout/> </ProtectedRoute>} >
          <Route path="/" element={<ProtectedRoute> <Home /> </ProtectedRoute>} />
          <Route path="/categories" element={<ProtectedRoute> <Categories /> </ProtectedRoute>} />
          <Route path="/summary" element={<ProtectedRoute> <Summary /> </ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute> <Settings /> </ProtectedRoute>} />
          {localStorage.getItem("IS_SUPERUSER") === "true" && <Route path="/admin" element={<ProtectedRoute> <Admin /> </ProtectedRoute>} />}
        </Route>

        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
