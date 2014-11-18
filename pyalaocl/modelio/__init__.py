# coding=utf-8
try:
    # noinspection PyUnresolvedReferences
    from org.modelio.api.modelio import Modelio
    WITH_MODELIO = True
except:
    WITH_MODELIO = False

if WITH_MODELIO:

    __all__ = [

        #  ...
        # THIS LIST IS EXTENDED DYNAMICALLY
        #  ...

        #----------------------------------------------------------------------
        #  Instrumentation of Modelio collections
        #----------------------------------------------------------------------

        # Class.ownedAttribute.select(...)  # ocl expressions on collection

        #----------------------------------------------------------------------
        #  MetaClass and instrumentation of MetaClasses (aka SmClass)
        #----------------------------------------------------------------------

        # Class    # a meta class, not a meta class (CHANGE!!!)
        #   metaClass
        #   metaInterface
        #   metaName
        #   metaPackage
        #   metaFullName
        #   metaFactory
        #   .new( ... )
        #   ( ... )         # not on interface :-(
        #   allInstances()
        #   named( name )
        #   selectByAttribute( attribute, value )

        'MetaClass',
        #   allInstances()
        #   named( name )
        #   selectByAttribute(attribute, value)
        'isMetaClass',

        #----------------------------------------------------------------------
        #  MetaInterface and instrumentation of MetaInterfaces (JavaInterfaces)
        #----------------------------------------------------------------------

        'isMetaInterface',

        # IClass  # was Class  (CHANGE!!!)
        #   metaClass
        #   metaInterface
        #   metaName
        #   metaPackage
        #   metaFullName
        #   metaIsAbstract    # isAbstract
        #   metaSuper         # return an MetaInterface
        #   metaSub           # return MetaInterfaces
        #   metaCmsNode
        #   metaFactory
        #   new(...)
        #   allInstances()
        #   named(name)
        #   selectByAttribute(attribute, value)
        #
        #
        #
        #
        # is<Class>()

        'MetaInterface',
        #   allInstances()
        #   named( name )
        #   selectByAttribute(attribute, value)
        'isMetaInterface',


        #----------------------------------------------------------------------
        #  Define global function isKindOfMETACLASS, isTypeOfMETACLASS
        #----------------------------------------------------------------------

        # IsKindOfClass(value)
        # IsTypeOfClass(value)

        #----------------------------------------------------------------------
        #  Register isKindOf and isTypeOf to main ocl module
        #----------------------------------------------------------------------

    ]

    import inspect
    from pyalaocl import \
        asSet, Invalid, registerIsKindOfFunction, \
        registerIsTypeOfFunction
    from pyalaocl.injector import \
        export, methodOf,  readOnlyPropertyOf
    import pyalaocl.jython
    # noinspection PyUnresolvedReferences
    from org.modelio.vcore.smkernel.meta import SmClass
    # noinspection PyUnresolvedReferences
    from org.modelio.metamodel import Metamodel as ModelioMetamodel
    # noinspection PyUnresolvedReferences
    from org.modelio.metamodel.uml.infrastructure import Stereotype
    # noinspection PyUnresolvedReferences
    from java.lang import Class as JavaClass
    # noinspection PyUnresolvedReferences
    from org.modelio.metamodel.uml.infrastructure import Element
    # noinspection PyUnresolvedReferences
    from org.modelio.vcore.smkernel.mapi import MClass




    #--------------------------------------------------------------------------
    #  Helpers
    #--------------------------------------------------------------------------


    def _theSession():
        return Modelio.getInstance().getModelingSession()


    _UML_BPMN_FACTORY = _theSession().getModel()
    _ANALYST_FACTORY = _theSession().getRequirementModel()


    def _getFactory(metaInterface):
        method_name = 'create' + metaInterface.metaName
        if hasattr(_UML_BPMN_FACTORY, method_name):
            return _UML_BPMN_FACTORY
        if hasattr(_ANALYST_FACTORY, method_name):
            return _ANALYST_FACTORY
        return None

    #--------------------------------------------------------------------------
    #  Instrumentation of Modelio collections
    #--------------------------------------------------------------------------


    def _addOCLSequenceOperationsOnModelioList():
        # noinspection PyUnresolvedReferences
        from org.eclipse.emf.common.util import EList
        # noinspection PyUnresolvedReferences
        from org.modelio.vcore.smkernel import SmList
        # noinspection PyUnresolvedReferences
        from org.modelio.vcore.smkernel import SmConstrainedList

        MODELIO_LISTS = [
            # FIXME: useless as addSuperClass does not works with inheritance
            # Another solution should probably be find
            # noinspection PyUnresolvedReferences
            EList,

            SmList,
            SmConstrainedList,
        ]

        print 'pyalaocl.modelio:'
        print '    Injecting Seq methods in Modelio list classes ... ',
        pyalaocl.injector.addSuperclass(
            pyalaocl.jython.JavaListExtension, MODELIO_LISTS)
        print 'done'


    def _selectByAttribute(cls, attribute, value):
            """
            Return the list of all the instances that have the
            property set to the given value.
            NOTE: Not sure how to deal with property that are not string.
            (MClass|Class)*String*String -> List(MObject)
            EXAMPLES
              selectedInstances(DataType,"Name","string")
            """
            return asSet(_theSession().findByAtt(cls, attribute, value))




    #--------------------------------------------------------------------------
    #  MetaClass and instrumentation of MetaClasses (aka SmClass)
    #--------------------------------------------------------------------------

    def _addGlobalNameOfMetaMetaClasses():
        for meta_class in MetaClass.allInstances():
            name = meta_class.name
            export(globals(), name, meta_class)


    @readOnlyPropertyOf(SmClass)
    def metaClass(metaClass):
        return metaClass

    @readOnlyPropertyOf(SmClass)
    def metaInterface(metaClass):
        return metaClass.javaInterface

    @readOnlyPropertyOf(SmClass)
    def metaName(metaClass):
        return metaClass.javaInterface.metaName

    @readOnlyPropertyOf(SmClass)
    def metaPackage(metaClass):
        return metaClass.javaInterface.metaPackage

    @readOnlyPropertyOf(SmClass)
    def metaFullName(metaClass):
        return metaClass.javaInterface.metaFullName


    @readOnlyPropertyOf(SmClass)
    def metaFactory(metaClass):
        return metaClass.javaInterface.metaFactory

    @methodOf(SmClass)
    def new(metaClass, *args, **kwargs):
        return metaClass.javaInterface.new(*args, **kwargs)

    @methodOf(SmClass)
    def __call__(metaClass, *args, **kwargs):
        return metaClass.javaInterface.new(*args, **kwargs)

    @methodOf(SmClass)
    def allInstances(metaClass):
        return metaClass.javaInterface.allInstances()

    @methodOf(SmClass)
    def named(metaClass, name):
        return metaClass.javaInterface.named(name)

    @methodOf(SmClass)
    def selectByAttribute(metaClass, attribute, value):
        # TODO: check if extensions needed for added attributes ?
        return metaClass.javaInterface.selectByAttribute(attribute, value)


    class MetaClass:

        @classmethod
        def allInstances(cls):
            return asSet(SmClass.getRegisteredClasses())

        @classmethod
        def named(cls, name):
            return ModelioMetamodel.getMClass(name)

        @classmethod
        def selectByAttribute(cls, attribute, value):
            return cls.allInstances().select(
                lambda mc: getattr(mc,attribute) == value)

    def isMetaClass(value):
        return isinstance(value, SmClass)




    #--------------------------------------------------------------------------
    #  MetaInterface and instrumentation of MetaInterfaces (i.e.JavaInterfaces)
    #--------------------------------------------------------------------------


    def _addGlobalNameOfMetaInterfaces():
        for meta_class in MetaClass.allInstances():
            name = meta_class.name
            export(globals(), name, meta_class)
            export(globals(), 'I' + name, meta_class.javaInterface)


    def _addFeaturesToAllMetaInterfaces():

        def _new(cls, *args, **kwargs):
            method = getattr(cls.metaFactory, 'create' + cls.metaName)
            return method(*args, **kwargs)

        def _allInstances(cls):
            """
            Return the set of all instances of a given metaclass or java meta
            interface.

            Provides both the direct instances but also instances of all
            subclasses. :return: The set all all instances, direct or indirect.
            :rtype: Set[MObject]
            """
            return asSet(_theSession().findByClass(cls))


        def _named(cls, name):
            """
            Return the only instance that have the given name.
            If there is more than one instance then raise an exception Invalid
            (MClass|Class)*String -> MObject|NameError
            """
            r = _theSession().findByAtt(cls, 'Name', name)
            if len(r) == 1:
                return r[0]
            elif len(r) == 0:
                raise Invalid('No %s named "%s"' % (cls, name))
            else:
                raise Invalid('More than one element named %s (%s elements)' \
                              % (name, str(len(r))))

        def _selectByAttribute(cls, attribute, value):
            """
            Return the list of all the instances that have the
            property set to the given value.
            NOTE: Not sure how to deal with property that are not string.
            (MClass|Class)*String*String -> List(MObject)
            EXAMPLES
              selectedInstances(DataType,"Name","string")
            """
            return asSet(_theSession().findByAtt(cls, attribute, value))

        # for some reason it is not possible to inject elements into MClasses

        print '    Injecting class methods/attributes in ' \
              + 'Modelio MetaInterfaces (%s) ...' \
                % MetaInterface.allInstances().size(),
        for mi in MetaInterface.allInstances():
            mi.metaClass = ModelioMetamodel.getMClass(mi)
            mi.metaInterface = mi
            mi.metaFullName = mi.getCanonicalName()
            mi.metaPackage = '.'.join(mi.metaFullName.split('.')[:-1])
            mi.metaName = mi.metaClass.name
            mi.metaIsAbstract = mi.metaClass.isAbstract()

            meta_super = mi.metaClass.super
            mi.metaSuper = \
                None if meta_super is None else meta_super.javaInterface
            mi.metaSubs = mi.metaClass.getSub(False).javaInterface.asSet()
            mi.metaAllSub = mi.metaClass.getSub(True).javaInterface.asSet()
            mi.metaCmsNode = mi.metaClass.isCmsNode()
            mi.metaFactory = _getFactory(mi)
            if mi.metaFactory is not None:
                mi.new = classmethod(_new)
            mi.allInstances = classmethod(_allInstances)
            mi.named = classmethod(_named)
            mi.selectByAttribute = classmethod(_selectByAttribute)
        print ' done'




    class MetaInterface(object):

        @classmethod
        def allInstances(cls):
            return MetaClass.allInstances().javaInterface.asSet()

        @classmethod
        def named(cls, name):
            return ModelioMetamodel.getMClass(name).getJavaInterface()

        @classmethod
        def selectByAttribute(cls, attribute, value):
            return cls.allInstances().select(
                lambda mc: getattr(mc, attribute) == value)

    # An adapted version of this function will be registered as isKind/TypeOf
    def isMetaInterface(value):
        if inspect.isclass(value):
            return issubclass(value, Element)
        else:
            return False

    #--------------------------------------------------------------------------
    #  Define global function isKindOfMETACLASS, isTypeOfMETACLASS
    #--------------------------------------------------------------------------



    def _addGlobalFunctionsIsXXXMETACLASS():
        # add global functions like isKindOfUseCase, isTypeOfClass, etc.

        # Not need to define this for metaClass, based on the name!
        # The argument metaInterface will disappear.
        def _newIsKindOfMETA(metaInterface):
            def isKindOfMETA(value):
                return isinstance(value, metaInterface)

            return isKindOfMETA

        def _newIsTypeOfMETA(metaInterface):
            meta_class = ModelioMetamodel.getMClass(metaInterface)

            def isTypeOfMETA(value):
                try:
                    return value.getMClass() is meta_class
                except:
                    return False

            return isTypeOfMETA


        for mi in MetaInterface.allInstances():
            export(globals(),
                   'isKindOf' + mi.metaName, _newIsKindOfMETA(mi))
            export(globals(),
                   'isTypeOf' + mi.metaName, _newIsTypeOfMETA(mi))


    #--------------------------------------------------------------------------
    #  Define operations on Modelio 'Element' metaclass
    #--------------------------------------------------------------------------

    def _addOperationsToModelioElementMetaClass():

        # noinspection PyUnresolvedReferences
        from org.modelio.metamodel.uml.infrastructure import Element

        print "    Adding object methods to Element ...",
        # Element.MetaInterface = property(_getMetaInterface)
        # TODO: remove if it remains useless
        print 'done'









    #--------------------------------------------------------------------------
    #  Define global level functions get access to modelio metamodel
    #--------------------------------------------------------------------------



    def theMetamodelExtensions():
        """ TODO, Warning this is not a list!
        """
        return _theSession().getMetamodelExtensions()



    #--------------------------------------------------------------------------
    #  Register isKindOf and isTypeOf to main ocl module
    #--------------------------------------------------------------------------

    def _registerIsKindTypeOfFunctions():
        def _isKindOf(element, mClassOrMInterface):
            """ Check if the element is a direct  or indirect instance of a MClass
                or interface. Use isTypeOf to test if the type is exactly
                the one specified.
                EXAMPLES
                  print isKindOf(instanceNamed(DataType,"string"),Element)
                  print isKindOf(instanceNamed(DataType,"string"),UseCase)
            """
            if isinstance(mClassOrMInterface, MClass):
                mClassOrMInterface = mClassOrMInterface.getJavaInterface()
            return isinstance(element, mClassOrMInterface)


        def _isTypeOf(element, mClassOrMInterface):
            """ Check if the element has exactly the type specified, not one of
                its subtype. Use isKindOf to test if the type is exactly the one
                specified.
                EXAMPLES
                  print isTypeOf(instanceNamed(DataType,"string"),DataType)
                  print isTypeOf(instanceNamed(DataType,"string"),Element)
            """
            if isinstance(mClassOrMInterface, JavaClass):
                mClassOrMInterface = \
                    ModelioMetamodel.getMClass(mClassOrMInterface)
            try:
                return element.getMClass() is mClassOrMInterface
            except:
                return False

        def _isTypeOfMetaInterface(value1, value2):
            if value2 is not MetaInterface:
                return False
            return isMetaInterface(value1)

        def _isTypeOfMetaClass(value1, value2):
            if value2 is not MetaClass:
                return False
            return isMetaClass(value1)

        print '    Registering Modelio isKindOf/isTypeOf functions ...',
        registerIsKindOfFunction(_isKindOf)
        registerIsTypeOfFunction(_isTypeOf)
        # The function works both for Kind and Type since no hierarchy
        registerIsKindOfFunction(_isTypeOfMetaInterface)
        registerIsTypeOfFunction(_isTypeOfMetaInterface)
        # The function works both for Kind and Type since no hierarchy
        registerIsKindOfFunction(_isTypeOfMetaClass)
        registerIsTypeOfFunction(_isTypeOfMetaClass)
        print 'done'








    _addOCLSequenceOperationsOnModelioList()
    _addFeaturesToAllMetaInterfaces()
    _addOperationsToModelioElementMetaClass()
    _addGlobalFunctionsIsXXXMETACLASS()
    _registerIsKindTypeOfFunctions()
    _addGlobalNameOfMetaInterfaces()
    _addGlobalNameOfMetaMetaClasses()
