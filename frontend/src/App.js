import Main from './components/Main';
import { Navigate, Routes, Route } from 'react-router-dom';
import './App.css'

function App() {
  return (
    <div className='wrapper'>
      <Routes>
        <Route path="/" element={<Main/>} exact/>
      </Routes>
    </div>
  )
}

export default App;
