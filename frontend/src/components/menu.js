// src/components/Menu.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Menu = () => {
  const [menuItems, setMenuItems] = useState([]);

  useEffect(() => {
    axios.get('/api/menu-items/')
      .then(response => {
        setMenuItems(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the menu items!", error);
      });
  }, []);

  return (
    <div>
      <h1>Menu</h1>
      <ul>
        {menuItems.map(item => (
          <li key={item.name}>
            <img src={item.image} alt={item.name} />
            <h2>{item.name}</h2>
            <p>{item.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Menu;
