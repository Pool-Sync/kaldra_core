/**
 * 4IAM.AI — Nav Component (Placeholder)
 * Status: Structure only — no logic implemented
 * 
 * Main navigation component for header
 * TODO: Implement navigation with active states and routing
 */

import Link from 'next/link';

export default function Nav() {
    return (
        <nav className="flex gap-6">
            {/* TODO: Add active state styling */}
            {/* TODO: Add dropdown menus for product categories */}

            <Link href="/dashboard" className="hover:text-blue-600">
                Dashboard
            </Link>

            <Link href="/signals" className="hover:text-blue-600">
                Signals
            </Link>

            <Link href="/insights" className="hover:text-blue-600">
                Insights
            </Link>

            <Link href="/explorer" className="hover:text-blue-600">
                Explorer
            </Link>

            {/* TODO: Add products dropdown */}
            <div className="relative">
                <button className="hover:text-blue-600">Products ▾</button>
                {/* TODO: Add dropdown menu */}
            </div>
        </nav>
    );
}
