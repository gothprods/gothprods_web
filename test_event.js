// Just a logic check: defer scripts execute after DOM parsing.
// If the document is already parsed, DOMContentLoaded might have fired or will fire immediately.
// Actually, defer scripts execute right BEFORE DOMContentLoaded.
