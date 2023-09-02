import './App.css';
import logo from './asset/logo.png';
import MenuContainer from './Components/MenuContainer';
import {
  Person,
  Add
} from '@mui/icons-material';
import InstagramIcon from '@mui/icons-material/Instagram';
import ShareIcon from '@mui/icons-material/Share';
import BackupIcon from '@mui/icons-material/Backup';
import VolunteerActivismIcon from '@mui/icons-material/VolunteerActivism';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    var menuitems = document.querySelectorAll('.iconcontainer')
    function gotolink(n){
    if(n === 4){
      window.location.href = 'https://www.instagram.com/pranavkdileep/'
    }
    }
    menuitems.forEach((item, index) => {
      item.addEventListener('click', () => {
        //only one time
        gotolink(index)
      })
    })
    
  }, [])
  return (
    <div className="App">
      <div className="menuContainer">
        <img src={logo} alt="logo" className="logo"/>
        <div className="menu">
          <div>
            <MenuContainer icon={<Person/>}/>
            <MenuContainer icon={<BackupIcon/>}/>
          </div>
          <div>
            <MenuContainer icon={<VolunteerActivismIcon/>}/>
            <MenuContainer icon={<ShareIcon/>}/>
            <MenuContainer icon={<InstagramIcon/>}/>
          </div>
          <MenuContainer icon={<Add/>}/>
          </div>
        </div>
        <main></main>
    </div>
  );
}

export default App;
