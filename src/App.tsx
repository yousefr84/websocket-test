import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import {SignIn} from "./components/SignIn.tsx";
import {SignUp} from "./components/SignUp.tsx";
import {Websocket} from "./components/Websocket.tsx";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path={'/'} element={<SignIn/>}></Route>
          <Route path={'/SignUp'} element={<SignUp/>}></Route>
          <Route path={'/websocket'} element={<Websocket/>}></Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
