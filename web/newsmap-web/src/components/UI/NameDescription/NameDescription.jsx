import React from 'react';
import cl from './NameDescription.module.css'

const NameDescription = () => {
    return (
        <div className={cl.NameDescription}>
            <h2>NewsMap</h2>
            <p className={cl.text}>Made as a diploma project by <a href={"https://t.me/n0862"} style={{fontWeight: "bold", textDecoration: "none", color: "inherit" }} target="_blank">@n0862</a></p>
        </div>
    );
};

export default NameDescription;