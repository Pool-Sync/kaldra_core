/**
 * KALDRA Explorer - Layout
 * 
 * Base layout for the Explorer module.
 */

export default function ExplorerLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
            {children}
        </div>
    );
}
