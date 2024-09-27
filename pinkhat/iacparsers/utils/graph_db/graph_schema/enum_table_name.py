import ast
from enum import Enum


class TableName(Enum):
    BoolOp = ast.BoolOp.__name__
    NamedExpr = ast.NamedExpr.__name__
    BinOp = ast.BinOp.__name__
    UnaryOp = ast.UnaryOp.__name__
    Lambda = ast.Lambda.__name__
    IfExp = ast.IfExp.__name__
    Dict = ast.Dict.__name__
    Set = ast.Set.__name__
    ListComp = ast.ListComp.__name__
    SetComp = ast.SetComp.__name__
    DictComp = ast.DictComp.__name__
    GeneratorExp = ast.GeneratorExp.__name__
    Await = ast.Await.__name__
    Yield = ast.Yield.__name__
    YieldFrom = ast.YieldFrom.__name__
    Compare = ast.Compare.__name__
    Call = ast.Call.__name__
    FormattedValue = ast.FormattedValue.__name__
    JoinedStr = ast.JoinedStr.__name__
    Constant = ast.Constant.__name__
    Attribute = ast.Attribute.__name__
    Subscript = ast.Subscript.__name__
    Starred = ast.Starred.__name__
    Name = ast.Name.__name__
    List = ast.List.__name__
    Tuple = ast.Tuple.__name__
    Slice = ast.Slice.__name__
    Module = ast.Module.__name__
    FunctionDef = ast.FunctionDef.__name__
    AsyncFunctionDef = ast.AsyncFunctionDef.__name__
    ClassDef = ast.ClassDef.__name__
    Return = ast.Return.__name__
    Delete = ast.Delete.__name__
    Assign = ast.Assign.__name__
    TypeAlias = ast.TypeAlias.__name__
    AugAssign = ast.AugAssign.__name__
    AnnAssign = ast.AnnAssign.__name__
    For = ast.For.__name__
    AsyncFor = ast.AsyncFor.__name__
    While = ast.While.__name__
    If = ast.If.__name__
    With = ast.With.__name__
    AsyncWith = ast.AsyncWith.__name__
    Match = ast.Match.__name__
    Raise = ast.Raise.__name__
    Try = ast.Try.__name__
    TryStar = ast.TryStar.__name__
    Assert = ast.Assert.__name__
    Import = ast.Import.__name__
    ImportFrom = ast.ImportFrom.__name__
    Global = ast.Global.__name__
    Nonlocal = ast.Nonlocal.__name__
    Expr = ast.Expr.__name__
    Pass = ast.Pass.__name__
    Break = ast.Break.__name__
    Continue = ast.Continue.__name__
    arg = ast.arg.__name__
    keyword = ast.keyword.__name__
    ExceptHandler = ast.ExceptHandler.__name__
    Is = ast.Is.__name__
    NotEq = ast.NotEq.__name__
    comprehension = ast.comprehension.__name__
