import React from 'react';
import cl from './Article.module.css'


const Article = (props) => {
    return (
        <div className={cl.article}>
            <p><strong>ID:</strong> {props.article.article_id}</p>
            <p><strong>TITLE:</strong> {props.article.title}</p>
            <p><strong>PROVIDER:</strong> {props.article.news_provider_name}</p>
            <p><strong>TIME PUBLISHED:</strong> {props.article.time_published}</p>
            <p><strong>TAGS:</strong> {props.article.tags}</p>
            <a href={props.article.link}>GO TO PAGE</a>
        </div>
    );
};

export default Article;