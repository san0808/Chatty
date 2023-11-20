import React from 'react'
import styles from '../styles/Home.module.css'
function NavTop() {
  return (
    <div className={styles.topnav}>
        <div className = {styles.navlogo}>
          <a href="/">Chatty</a>
        </div>
        <div className = {styles.navlinks}>
          <a href="https://elfin-fireman-b6a.notion.site/stimuler-460c470bc0a247aba5ec7c98acf445a8?pvs=4" target="_blank">Docs</a>
          <a href="https://github.com/san0808/Chatty" target="_blank">GitHub</a>
        </div>       
      </div>
  )
}

export default NavTop