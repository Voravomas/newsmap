import React from 'react';
import classes from './DateInput.module.css'
import {MIN_DATE, MAX_DATE} from "../../../constants";

const DateInput = React.forwardRef((props,  ref) => {
    return (
        <div className={classes.datePicker}>
            <p className={classes.fromToText}>{props.dateInputName}</p>
            <input
                type="date"
                id={props.dateInputName}
                name={props.dateInputName}
                value={MIN_DATE}
                min={MIN_DATE}
                max={MAX_DATE}
                ref={ref}
                {...props}
            />
        </div>
    );
});

export default DateInput;
