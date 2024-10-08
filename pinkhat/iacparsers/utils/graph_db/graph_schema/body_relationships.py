from pinkhat.iacparsers.utils.graph_db.graph_schema.enum_table_name import TableName

BODY_RELATIONSHIPS = [
    TableName.AnnAssign.value,
    TableName.Assign.value,
    TableName.Assert.value,
    TableName.AsyncFunctionDef.value,
    TableName.ClassDef.value,
    TableName.Expr.value,
    TableName.For.value,
    TableName.FunctionDef.value,
    TableName.Global.value,
    TableName.If.value,
    TableName.Import.value,
    TableName.ImportFrom.value,
    TableName.Lambda.value,
    TableName.Pass.value,
    TableName.Try.value,
    TableName.Raise.value,
    TableName.Return.value,
    TableName.While.value,
    TableName.With.value,
]
