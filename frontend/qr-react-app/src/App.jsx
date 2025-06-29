import { Routes, Route } from 'react-router-dom'
import LoginRegister from './components/LoginRegister'
import MainPage from './components/MainPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginRegister />} />
      <Route path="/dashboard" element={<MainPage />} />
    </Routes>
  )
}

export default App