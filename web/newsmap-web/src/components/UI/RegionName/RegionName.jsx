import React from 'react';
import cl from "./RegionName.module.css"

const RegionName = ({name}) => {
    function splitRegionName(name) {
        let spl = name.split(" ");
        return [spl.slice(0, -1).join(' '), spl.slice(-1)[0]];
    }
    let firstPart, secondPart;
    [firstPart, secondPart] = splitRegionName(name);
    return (
        <div className={cl.RegionName}>
            <h2>{firstPart}<br/>{secondPart}</h2>
        </div>
    );
};

export default RegionName;