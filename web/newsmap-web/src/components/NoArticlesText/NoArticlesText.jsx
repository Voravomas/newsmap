import React from 'react';
import classes from "./NoArticlesText.module.css"
import { ReactComponent as Search } from './Search.svg'


const NoArticlesText = () => {
    return (
        <div className={classes.NoArticlesText}>
            <h3 style={{textAlign: "center", color: "#768396"}}>Немає статей<br/>по регіону</h3>
            <div style={{display: "flex", justifyContent: "center"}}><Search width="4rem" height="4rem" stroke-width="2" color="#768396"/></div>
        </div>
    );
};

export default NoArticlesText;