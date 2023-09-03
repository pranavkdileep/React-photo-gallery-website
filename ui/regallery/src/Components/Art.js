import React from 'react'

function Art({size,d_icon}) {
  return (
    <div className={`art ${size}`}>
      <img src="https://plus.unsplash.com/premium_photo-1677851913233-0758697643c7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80" alt="art"/>
      <div className='artInfo'>
        <h4>Art Name</h4>
        <div className="d_icon">
          {d_icon}
          </div>
        </div>
    </div>
  )
}

export default Art