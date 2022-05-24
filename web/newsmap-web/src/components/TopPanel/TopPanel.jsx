import React from 'react';
import cl from './TopPanel.module.css'
import NameDescription from "../UI/NameDescription/NameDescription";
import ArticleFilter from "../ArticleFilter/ArticleFilter";

const TopPanel = ({timeConfig, setTimeConfig, totalArticles,
                      setTotalArticles, setArticles, setSelectedRegion}) => {
    return (
        <div className={cl.TopPanel}>
            <NameDescription/>
            <ArticleFilter
                timeConfig={timeConfig}
                totalArticles={totalArticles}
                setTimeConfig={setTimeConfig}
                setArticles={setArticles}
                setSelectedRegion={setSelectedRegion}
                setTotalArticles={setTotalArticles}/>
        </div>
    );
};

export default TopPanel;