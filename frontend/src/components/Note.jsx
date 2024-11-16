function Note({note, onDelete}) {
    return (
        <div>
            <p className="note-title">{note.title}</p>
            <p className="note-content">{note.content}</p>
            <button className="note-delete" onClick={() => onDelete(note.id)}>Delete</button>
        </div>
    )
}

export default Note