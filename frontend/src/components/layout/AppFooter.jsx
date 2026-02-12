import { COLORS } from '../../theme/colors';
import './AppFooter.css';

const AppFooter = () => {
    return (
        <footer className="app-footer" style={{ backgroundColor: COLORS.BLACK }}>
            <div className="footer-container">
                <p style={{ color: COLORS.WHITE, margin: 0 }}>
                    © 2026 GEARVN. All rights reserved.
                </p>
            </div>
        </footer>
    );
};

export default AppFooter;
