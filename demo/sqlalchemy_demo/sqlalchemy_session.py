from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


DB_CONNECT='mssql+pyodbc://sa:CgSqlServerRoot2012@172.17.18.110/cgyypt?driver=ODBC+Driver+17+for+SQL+Server'

class CreateDB:

    def __init__(self, DB_URL=None):
        self.__db_url = DB_URL if DB_URL else DB_CONNECT
        self.__session = None

    def __enter__(self):
        print('----------------开启链接----------------')
        engine = create_engine(self.__db_url, echo=True)
        engine.execution_options(autocommit=True)
        session = sessionmaker(bind=engine)
        self.__session = session()
        self.__session.begin()
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('----------------关闭链接----------------')
        self.__session.close()


if __name__ == '__main__':
    sql = '''
        select scid,gpschyid,sclhid,f1=SUM(f1),sclh=MAX(sclh),clmc=replace(replace(replace(max(clmc),'螺纹钢',''),'盘螺',''),'盘圆',''),
        ggxh=MAX(ggxh),sxs=MAX(sxs),
        dyzl=max(dyzl),
        dyks=max(dyks),    
        a18=MAX(a18),a16=MAX(a16),a17=MAX(a17),
        a6=MAX(a6),a7=MAX(a7),a76=MAX(a76),
        a77=MAX(a77),a38=MAX(a38),a35=MAX(a35),
        a65=MAX(a65),a78=MAX(a78),a33=MAX(a33) from 
        (select a.scid,b.gpschyid,f1,b.sclhid,cldm,
        sclh=max(b.sclh),
        clmc=max(b.clmc),
        ggxh=max(b.ggxh),
        dyzl=(select dyzl from xs_dy_zbzs_sclh where pdid=9279992 and sclh=max(b.sclh)),
        dyks=(select dyks from xs_dy_zbzs_sclh where pdid=9279992 and sclh=max(b.sclh)),     
        sxs=(select sx_sxs from cl_csh_clxx where id=max(b.clid)),     
        a18=max(case a.zbid when 18 then (jyjg) else '' end),
        a16=max(case a.zbid when 16 then (jyjg) else '' end),
        a17=max(case a.zbid when 17 then (jyjg) else '' end),
        a6=max(case a.zbid when 6  then (jyjg) else '' end),
        a7=max(case a.zbid when 7  then (jyjg) else '' end),
        a76=max(case a.zbid when 76  then (jyjg) else '' end),
        a77=max(case a.zbid when 77  then (jyjg) else '' end),
        a38=max(case a.zbid when 38  then (jyjg) else '' end),
        a35=max(case a.zbid when 35  then (jyjg) else '' end),
        a65=max(case a.zbid when 65  then (jyjg) else '' end),
        a78=max(case a.zbid when 78  then (jyjg) else '' end),
        a33=max(case a.zbid when 33  then (jyjg) else '' end),
        AA=11 
        from ccp_gpsc_gphy_clmx a,
        (select b.kfid,b.kfmc,b.clid,sclhid=d.pdid,zghycs=d.zghycs,
        d.gpsclhid,
        d.gpschyid,c.sclh,c.cldm,c.clmc,c.ggxh,f1=count(*) 
        from cl_pdxs_xsgbd_fjmx a,cl_pdxs_xsgbd_clmx b,cl_pdxs_xszcd_clmx c,
        cl_pdkc_ccpscd_clmx d,cl_pdkc_ccpscd_fjmx e  
        where a.pdid=b.pdid and c.pdid=a.zcdid and b.clid=c.clid and a.pdid=9279992 and
        e.sclh in (select sclh from xs_dy_zbzs_sclh where pdid=9279992) and 
        d.sctm=c.sctm and d.pdid=e.pdid  and  LEFT(e.pdh,6)>='201811'
        and not b.clid in (select id from cl_csh_clxx where sx_ccp_pt_300=1)                                      
        group by b.kfid,b.kfmc,b.clid,d.pdid,d.zghycs,d.gpschyid,d.gpsclhid,c.sclh,c.cldm,c.clmc,c.ggxh) b 
        where a.scid=b.gpsclhid 
        group by a.scid,b.gpschyid,f1,b.sclhid,zghycs,cldm) A1
        group by scid,gpschyid,sclhid,sclh,cldm          
        order by sclh
    '''

    with CreateDB() as db:
        db: Session
        try:
            db.add()
        except Exception:
            db.rollback()
        result = db.execute(sql)
        print(result.all())
