// components/grading/DocumentViewer.tsx
interface DocumentViewerProps {
    document: {
      title: string;
      content: string;
    }
  }
  
  const DocumentViewer = ({ document }: DocumentViewerProps) => {
    return (
      <div className="prose max-w-none">
        <h3 className="text-lg font-medium mb-4">{document.title}</h3>
        <div className="whitespace-pre-wrap font-mono text-sm">
          {document.content}
        </div>
      </div>
    )
  }
  
  export default DocumentViewer