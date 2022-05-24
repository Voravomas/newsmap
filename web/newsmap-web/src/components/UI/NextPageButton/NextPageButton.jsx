import React from 'react';
import classes from "./NextPageButton.module.css";
import { ReactComponent as ArrowLeft } from './ArrowLeft.svg'
import { ReactComponent as ArrowRight } from './ArrowRight.svg'

const NextPageButton = ({position, onClick}) => {
    return (
        <div>
            {
                position === "r"
                ? <button onClick={onClick} className={classes.NextPageButton}>
                        <ArrowRight width="1rem" stroke-width="2" color="#768396"/>
                </button>
                : <button onClick={onClick} className={classes.NextPageButton}>
                        <ArrowLeft width="1rem" stroke-width="2" color="#768396"/>
                </button>
            }
        </div>);
};

export default NextPageButton;
