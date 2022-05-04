import React from 'react';
import ArticleListByRegion from "./ArticleListByRegion";
import OBLAST_TO_NUM from "../constants"
//console.log(OBLAST_TO_NUM[article_region])

const ArticleModule = ({articles}) => {
    return (
        <div>
            {Object.entries(articles).map(([article_region,article_value], i) =>
                    <ArticleListByRegion
                        key={i}
                        articles={article_value}
                        regionTitle={OBLAST_TO_NUM[article_region]}/>
                )}
        </div>
    );
};

export default ArticleModule;