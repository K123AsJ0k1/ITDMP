import Main from './components/Main';
import { Navigate, Routes, Route } from 'react-router-dom';
import './App.css'
import Header from './components/Header';

function App() {
  return (
    <div className='wrapper'>
      <Header/>
      <Routes>
        <Route path="/" element={<Main/>} exact/>
      </Routes>
    </div>
  )
}

export default App;
