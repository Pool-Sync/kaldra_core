/**
 * 4IAM.AI — Sidebar Component (Placeholder)
 * Status: Structure only — no logic implemented
 * 
 * Collapsible sidebar navigation for dashboard views
 * TODO: Implement sidebar with navigation tree and collapse functionality
 */

export default function Sidebar() {
    return (
        <aside className="w-64 border-r min-h-screen p-4">
            <div className="space-y-4">
                {/* TODO: Add navigation sections */}
                <div>
                    <h3 className="font-bold mb-2">Dashboard</h3>
                    <ul className="space-y-1 text-sm">
                        <li className="text-gray-400">TODO: Dashboard links</li>
                    </ul>
                </div>

                <div>
                    <h3 className="font-bold mb-2">Products</h3>
                    <ul className="space-y-1 text-sm">
                        <li className="text-gray-400">• Alpha</li>
                        <li className="text-gray-400">• GEO</li>
                        <li className="text-gray-400">• Product</li>
                        <li className="text-gray-400">• Safeguard</li>
                    </ul>
                </div>

                <div>
                    <h3 className="font-bold mb-2">Intelligence</h3>
                    <ul className="space-y-1 text-sm">
                        <li className="text-gray-400">• Signals</li>
                        <li className="text-gray-400">• Insights</li>
                        <li className="text-gray-400">• Explorer</li>
                    </ul>
                </div>
            </div>
        </aside>
    );
}
