import React from 'react';
import classes from './dateInput.module.css'
import {MIN_DATE, MAX_DATE} from "../../../constants";

const DateInput = React.forwardRef((props, ref) => {
    return (
        <div className={classes.datePicker}>
            <input
                type="date"
                id="start"
                name="time_start"
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
