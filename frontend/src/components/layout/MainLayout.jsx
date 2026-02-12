import React from 'react';
import AppHeader from './AppHeader';
import AppFooter from './AppFooter';
import CategorySidebar from '../sidebar/CategorySidebar';
import '../../styles/layout.css';

const MainLayout = ({ children, showSidebar = false }) => {
    return (
        <div className="homepage-layout">
            <AppHeader />

            <div className="homepage-content">
                {showSidebar && (
                    <div className="sidebar-container">
                        <CategorySidebar />
                    </div>
                )}
                <div className={showSidebar ? "main-content" : "main-content full-width"}>
                    {children}
                </div>
            </div>

            <AppFooter />
        </div>
    );
};

export default MainLayout;
