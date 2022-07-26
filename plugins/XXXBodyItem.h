#ifndef CNOID_IRSL_XXX_PLUGIN_BODY_ITEM_H
#define CNOID_IRSL_XXX_PLUGIN_BODY_ITEM_H

#include <cnoid/Item>
#include <cnoid/Body>

#include <cnoid/LocatableItem>
#include <cnoid/RenderableItem>
#include "exportdecl.h"

namespace cnoid {
class ItemManager;
class ItemFileIO;
class XXXSceneBody;

//class CNOID_EXPORT XXXBodyItem : public Item, public LocatableItem, public RenderableItem
//class CNOID_EXPORT XXXBodyItem : public Item, public LocatableItem, public RenderableItem
class CNOID_EXPORT XXXBodyItem : public Item, public RenderableItem
{
public:
    static void initializeClass(ExtensionManager* ext);

    // The following functions are Implemented in XXXBodyItemFileIO.cpp
    static void registerXXXBodyItemFileIoSet(ItemManager* im);
    //! The actual type of the IO object returned by this function is XXXBodyItemBodyFileIO.
    //static ItemFileIO* bodyFileIO();
    static ItemFileIO* meshFileIO();

    XXXBodyItem();
    XXXBodyItem(const std::string& name);
    XXXBodyItem(const XXXBodyItem& org);
    virtual ~XXXBodyItem();

    virtual bool setName(const std::string& name) override;

    Body* body() const;
    void setBody(Body* body);

    // API for a composite body
    // The following body and link pair is basically determined by
    // the parent-child relationship in the item tree
    //XXXBodyItem* parentXXXBodyItem();

    enum ModelUpdateFlag {
        LinkSetUpdate = 1 << 0,
        DeviceSetUpdate = 1 << 1,
        DeviceSpecUpdate = 1 << 2,
        ShapeUpdate = 1 << 3
    };
    SignalProxy<void(int flags)> sigModelUpdated();
    void notifyModelUpdate(int flags);

    /**
       This signal is emitted when there is a change in "kinematic" state such as joint angle of robot,
       joint angular velocity, root position / posture. Item :: sigUpdated () is assumed to be
       a case where the model itself is changed, and you have to distinguish them.
    */
    SignalProxy<void()> sigKinematicStateChanged();
    void notifyKinematicStateChange(
        bool requestFK = false, bool requestVelFK = false, bool requestAccFK = false);
    void notifyKinematicStateChange(
        Connection& connectionToBlock,
        bool requestFK = false, bool requestVelFK = false, bool requestAccFK = false);
    void notifyKinematicStateChangeLater(
        bool requestFK = false, bool requestVelFK = false, bool requestAccFK = false);
    void notifyKinematicStateChangeLater(
        Connection& connectionToBlock,
        bool requestFK = false, bool requestVelFK = false, bool requestAccFK = false);

    /**
       This signal is emitted when a kinematic state has been updated.
       In constrast to sigKinematicStateChange, this signal is emitted when a series of changes
       are finalized.
    */
    SignalProxy<void()> sigKinematicStateUpdated();
    void notifyKinematicStateUpdate(bool doNotifyStateChange = true);

    // LocatableItem function
    //virtual LocationProxyPtr getLocationProxy() override;
    //bool isLocationEditable() const;
    //void setLocationEditable(bool on);
    //LocationProxyPtr createLinkLocationProxy(Link* link);

    // RenderableItem function
    virtual SgNode* getScene() override;
    XXXSceneBody* sceneBody();

    float transparency() const;
    void setTransparency(float t);

    class Impl;

protected:
    virtual Item* doDuplicate() const override;
    virtual bool doAssign(const Item* item) override;
    virtual void onTreePathChanged() override;
    virtual void onConnectedToRoot() override;
    virtual void doPutProperties(PutPropertyFunction& putProperty) override;

private:
    Impl* impl;
};

typedef ref_ptr<XXXBodyItem> XXXBodyItemPtr;

}

#endif