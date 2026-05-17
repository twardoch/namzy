// this_file: namzy-cpp/src/namzy.cpp
#include "namzy.h"
#include "mangle.h"

Namzy::Namzy(quint64 seed)
    : m_rng(seed)
{
}

QString Namzy::generate()
{
    return buildName(m_rng);
}

QStringList Namzy::generateMany(int count)
{
    QStringList out;
    out.reserve(count);
    for (int i = 0; i < count; ++i) {
        out.append(buildName(m_rng));
    }
    return out;
}
