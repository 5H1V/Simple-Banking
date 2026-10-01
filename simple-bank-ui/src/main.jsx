import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import './index.css'
import AccountsPage from './components/AccountsPage.jsx'
import App from './App.jsx'
import TransactionsPage from './components/TransactionsPage.jsx'
import WelcomePage from './components/WelcomePage.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/users" element={<App />} />
        <Route path="/accounts" element={<AccountsPage />} />
        <Route path="/transactions" element={<TransactionsPage />} />
        <Route path="*" element={
          <main className="not-found">
            <h1>Page not found</h1>
            <p>The page you requested does not exist.</p>
            <Link to="/">Return to the welcome page</Link>
          </main>
        } />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
