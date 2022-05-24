import React from 'react';
import {getCurrentPageString} from "../../../utils/getCurrentPageString";
import cl from "./PageNumber.module.css"

const PageNumber = ({requestOffset, totalArticlesInRegion}) => {
    return (
        <div>
            <p className={cl.PageNumber}>{getCurrentPageString(requestOffset, totalArticlesInRegion)}</p>
        </div>
    );
};

export default PageNumber;